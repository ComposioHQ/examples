import "dotenv/config";
import { ChatOpenAI } from "@langchain/openai";
import { createOpenAIFunctionsAgent, AgentExecutor } from "langchain/agents";
import { LangchainToolSet } from "composio-core";
import { pull } from "langchain/hub";
import { setupUserConnectionIfNotExists, getEmailPrompts } from "./utils.js";
import ora from "ora";
const llm = new ChatOpenAI({ apiKey: process.env.OPENAI_API_KEY });

const run = async () => {
  const toolset = new LangchainToolSet({
    apiKey: process.env.COMPOSIO_API_KEY,
  });
  await setupUserConnectionIfNotExists(
    process.env.entityId || "default",
    "gmail",
    toolset
  );
  const { emailContent, recipientEmail } = await getEmailPrompts();
  const tools = await toolset.getTools({ actions: ["GMAIL_SEND_EMAIL"] });

  const agent = await createOpenAIFunctionsAgent({
    llm,
    tools,
    prompt: await pull("hwchase17/openai-functions-agent"),
  });
  const spinner = ora("Sending email using Gmail and Composio").start();

  const response = await new AgentExecutor({ agent, tools }).invoke({
    input: `Send email to ${recipientEmail} with content: ${emailContent}. Add relevant subject.`,
  });

  spinner.stop();

  console.log("\nAgent Response:", response.output, "\n");
};

run().catch(console.error);
