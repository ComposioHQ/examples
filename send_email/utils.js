import inquirer from "inquirer";

export async function getEmailPrompts() {
  const { user_prompt_email_content, user_prompt_recipient_email } =
    await inquirer.prompt([
      {
        type: "input",
        name: "user_prompt_email_content",
        message: "What would you like to write in the email?",
      },
      {
        type: "input",
        name: "user_prompt_recipient_email",
        message: "Who would you like to send the email to?",
      },
    ]);

  return {
    emailContent: user_prompt_email_content,
    recipientEmail: user_prompt_recipient_email,
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
