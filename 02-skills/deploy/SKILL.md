---
allowed-tools: []
---

# Deploy to Vercel
1. Run `vercel --prod` from the project root
2. After deployment, verify Deployment Protection is disabled: check Settings → Deployment Protection
3. Test the webhook endpoint with: `curl -X POST <deployment-url>/api/webhook -H 'Content-Type: application/json' -d '{"test": true}'`
4. Report the deployment URL and test result
