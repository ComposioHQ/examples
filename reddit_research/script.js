import { openai } from "@ai-sdk/openai";
import { VercelAIToolSet } from "composio-core";
import dotenv from "dotenv";
import { generateText } from "ai";
import ora from "ora";
import readline from "readline";

dotenv.config();

const appName = "reddit";

async function setupUserConnectionIfNotExists(entityId, toolset) {
  const entity = await toolset.client.getEntity(entityId);
  try{
    const connection = await entity.getConnection({
      app: appName,
    });
    return connection;

  } catch{
    const newConnection = await entity.initiateConnection({
      appName: appName,
      entity: entityId
    });
    console.log("Log in via: ", newConnection.redirectUrl);
    return await newConnection.waitUntilActive(100);
  }

}

async function run() {
  // Setup toolset
  const toolset = new VercelAIToolSet({
    apiKey: process.env.COMPOSIO_API_KEY,
  });

  // Create readline interface
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  // Get subreddit input from user
  const subreddit = await new Promise((resolve) => {
    rl.question('Enter the subreddit name (e.g., "developersIndia"): ', (answer) => {
      rl.close();
      resolve(`r/${answer}/`);
    });
  });
  process.env.entityId='Yo'
  // Setup entity and ensure connection
  const entityId = process.env.entityId;
  await setupUserConnectionIfNotExists(entityId, toolset);

  // Retrieve tools for the specified app
  const tools = await toolset.getTools({ apps: [appName] }, entityId);

  const spinner = ora("Researching subreddit using Reddit and Composio").start();

  // Generate text using the model and tools
  const output = await generateText({
    model: openai("gpt-4o"),
    streamText: false,
    tools: tools,
    prompt: `Research the subreddit ${subreddit} and provide a summary of the top posts.`,
    maxToolRoundtrips: 5,
  });
  const final_output = await generateText({
    model: openai("gpt-4o"),
    streamText: false,
    prompt: `This is the tool call: ${JSON.stringify(output.toolCalls)} and tool result: ${JSON.stringify(output.toolResults)}. Explain the results and outcomes to the user.`,
    maxToolRoundtrips: 5,
  });
  spinner.stop();

  console.log("\nAgent Response:", final_output.text, "\n");
}

run().catch(console.error);
