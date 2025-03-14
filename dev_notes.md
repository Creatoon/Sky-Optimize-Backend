## Obtaining Azure Access Token and Subscription ID

### Azure Access Token

To obtain the `AZURE_ACCESS_TOKEN`, use the following commands:

1. Log in to your Azure account:

   ```sh
   az login
   ```

2. Get the access token:
   ```sh
   az account get-access-token --resource=https://management.azure.com
   ```

### Azure Subscription ID

To find your `AZURE_SUBSCRIPTION_ID`, visit the [Azure Portal Subscriptions Page](https://portal.azure.com/#view/Microsoft_Azure_Billing/SubscriptionsBladeV2).

### Free Azure Services

You can explore all free services available for 12 months and on a monthly basis by visiting the [Azure Portal Free Services Page](https://portal.azure.com/#view/Microsoft_Azure_Billing/FreeServicesBlade).

### Microsoft Azure Founder's hub

To know the remaining credit and services offered to founders, visit the [Microsoft for Startups Founders Hub](https://foundershub.startups.microsoft.com/).
