import { openai } from "@ai-sdk/openai";
import { VercelAIToolSet } from "composio-core";
import dotenv from "dotenv";
import { generateText } from "ai";
import ora from "ora";
import readline from "readline";

dotenv.config();

const appName = "googlecalendar";
const toolset = new VercelAIToolSet({
  apiKey: process.env.COMPOSIO_API_KEY,
  entityId: process.env.entityId
});
async function setupUserConnectionIfNotExists(entityId) {
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
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  // Get date/time input from user
  const dateTime = await new Promise((resolve) => {
    rl.question('Enter the date and time (e.g., "2024-03-20 3:00 PM"): ', (answer) => {
      resolve(answer);
    });
  });

  // Get event description from user
  const eventDescription = await new Promise((resolve) => {
    rl.question('Enter the event description: ', (answer) => {
      rl.close();
      resolve(answer);
    });
  });

  const entityId = process.env.entityId;
  await setupUserConnectionIfNotExists(
    process.env.entityId, 
  );

  const tools = await toolset.getTools({ actions: ['GOOGLECALENDAR_QUICK_ADD'] }, entityId);

  const spinner = ora("Processing calendar request...").start();

  // Generate text using the model and tools
  const output = await generateText({
    model: openai("gpt-4o"),
    streamText: false,
    tools: tools,
    prompt: `Create a calendar event for ${dateTime} with the following description: ${eventDescription}. Check for any scheduling conflicts and suggest alternative times if needed.`,
    maxToolRoundtrips: 5,
  });
  const final_output = await generateText({
    model: openai("gpt-4o"),
    streamText: false,
    prompt: `Based on these calendar operations - Tool calls: ${JSON.stringify(output.toolCalls)} and results: ${JSON.stringify(output.toolResults)}, provide a user-friendly summary of what was scheduled or any conflicts found. Print the calendar link.`,
    maxToolRoundtrips: 5,
  });
  spinner.stop();

  console.log("\nCalendar Agent Response:", final_output.text, "\n");
}

run().catch(console.error);
