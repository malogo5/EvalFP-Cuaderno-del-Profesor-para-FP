#!/bin/bash
cd "/Users/isabel/Documents/Claude/Projects/Cuaderno del profesor/evalfp-app"
npx playwright test --reporter=list
echo ""
echo "Tests terminados. Cierra esta ventana cuando quieras."
read -p ""
