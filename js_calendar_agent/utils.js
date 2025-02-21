import inquirer from "inquirer";

export async function getRedditPrompts() {
  const { user_prompt_subreddit } = await inquirer.prompt([
    {
      type: "input",
      name: "user_prompt_subreddit",
      message: "Which subreddit would you like to research? (e.g. 'developersIndia')",
    }
  ]);

  return {
    subreddit: `r/${user_prompt_subreddit}/`
  };
}

export async function setupUserConnectionIfNotExists(
  entityId,
  appName,
  toolset
) {
  let connection;
  const entity = toolset.client.getEntity(entityId);
  try {
    connection = await entity.getConnection({ appName: appName });
  } catch (_) {
    connection = await entity.initiateConnection({ appName: appName });
    console.log(
      `\nPlease connect your ${
        appName.charAt(0).toUpperCase() + appName.slice(1)
      } account by clicking on the below link:\n\n`,
      connection.redirectUrl
    );
    return connection.waitUntilActive(60);
  }
  console.log("\n");
  return connection;
}
