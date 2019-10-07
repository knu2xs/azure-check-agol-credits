# Check AGOL Credits

Keeping track of ArcGIS Online credits, I am terrible at checking the ArcGIS Online organizations I am responsible for in time to submit the internal request to refresh the creits. Admittedly, I do work for Esri. Consequently, procuring additional credits is really little more than a process of submitting the request using the correct Microsoft Word Document form. There typically is a few days to a week until this happens, and in the meantime our organization usually is frozen - we cannot publish anything.

After this happend most recently, I decided to fix the situation using a reliable method of checking this weekly, an Azure Function. Two things consistently make me put off submitting the request _even when I do notice credits are low_ - finding the form, and remembering who to email it to. Hence, this script reminds me to refresh the credits when they are low, _and_ has the correct Microsoft Word Document attached to the email along with reminding me who to email it to in the body.

## Resources Used

The script expects the Word Document, the request form, is located at `./resources/subscription_requeset.docx`. There are quite a few other variables loaded, but all of these are loaded from environemnt variables. These include...

* `SENDGRID_KEY` - This is the Azure SendGrid key used to send the email, pretty much jsut a token. SendGrid is something you can sign up for just like any other service in Azure. Since with the free tier you get 25,000 emails per month, this typically is more than enough. 
* `AGOL_USERNAME` - This requires a User in the ArcGIS Online organization, and this is obvioiusly the username.
* `AGOL_PASSWORD` - The password for the ArcGIS Online user provided.
* `EMAIL_TO` - This is the email address where the notification will be sent. The way the script is currently set up, this also is populated as the _from_ address as well.
* `EMAIL_NAME_TO` - So something more then just an email address shows up, this is the name of the owner of the account associated with the _to_ email.
* `EMAIL_ADMIN` - This is the email address of the Amin to whom the completed form will be sent to. This email is provieded in the body of the email to make life a little easier.
* `EMAIL_ADMIN_NAME` - Just like before, this is the name of the Admin who owns the aforementioned email address.

Environment variables in Azure Functions are admitteldy a little confusing to understand from the [Azure documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python#environment-variables). During local testing execution these values are [loaded from the `Values` key in the `local.settings.json` file](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#local-settings-file). Once published, these values are loaded from the [Application Settings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings#settings) in the Azure Function. This means, for the function to work, you must add the same key value pairs to both the `Values` section in the `local.settings.json` file for testing, and the Application Settings for the Function in the Azure portal for production.

While this seems a little difficult to sort out at first, it does have a definite upside. None of your personal information nor 

## It IS Open Source

While this is a pretty custom workflow, this pattern of monitoring ArcGIS Online metrics using an Azure Function, and using a scheduled Azure Function to provide notificaiton with the right resources to address the issue, this is something much more universal. Since completely open source in every sense of the word, please feel free to use as much or as little of the code in this repo as you like. Obviously I will not really know if you don't give me credit, but if you do find this useful, and you use it, I appreaciate you giving me credit for it.
