#!/usr/bin/env node

const commands = {
    analyze() {
        console.log("🔍 Analizando proyecto...");
    },

    splitCss() {
        console.log("🎨 Extrayendo CSS...");
    },

    splitJs() {
        console.log("📦 Extrayendo JavaScript...");
    },

    architecture() {
        console.log("🏗️ Analizando arquitectura...");
    }
};

const command = process.argv[2];

if (!command) {
    console.log(`
Uso:

node scripts/refactor.js analyze
node scripts/refactor.js split-css
node scripts/refactor.js split-js
node scripts/refactor.js architecture
`);
    process.exit(0);
}

switch(command){

    case "analyze":
        commands.analyze();
        break;

    case "split-css":
        commands.splitCss();
        break;

    case "split-js":
        commands.splitJs();
        break;

    case "architecture":
        commands.architecture();
        break;

    default:
        console.log("Comando desconocido");
}
