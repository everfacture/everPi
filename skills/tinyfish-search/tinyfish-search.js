#!/usr/bin/env node

import https from "node:https";
import http from "node:http";

const API_KEY = process.env.TINYFISH_API_KEY;
if (!API_KEY) {
  console.error("✗ TINYFISH_API_KEY not set");
  console.error("  Add to ~/.zprofile: export TINYFISH_API_KEY=\"your-key\"");
  console.error("  Then run: source ~/.zprofile");
  process.exit(1);
}

const args = process.argv.slice(2);
let query = "";
let location = "";
let language = "";
let page = 0;
let content = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--location" && args[i + 1]) { location = args[++i]; }
  else if (args[i] === "--language" && args[i + 1]) { language = args[++i]; }
  else if (args[i] === "--page" && args[i + 1]) { page = parseInt(args[++i]); }
  else if (args[i] === "--content") { content = true; }
  else { query = query ? `${query} ${args[i]}` : args[i]; }
}

if (!query) {
  console.log("Usage: tinyfish-search.js <query> [--location US] [--language en] [--page 0] [--content]");
  console.log("\nExamples:");
  console.log('  tinyfish-search.js "web automation tools"');
  console.log('  tinyfish-search.js "python tutorial" --location US --language en');
  console.log('  tinyfish-search.js "best restaurants" --location FR --language fr');
  console.log('  tinyfish-search.js "news" --content');
  process.exit(1);
}

const params = new URLSearchParams({ query });
if (location) params.set("location", location);
if (language) params.set("language", language);
if (page) params.set("page", page.toString());

const url = `https://api.search.tinyfish.ai?${params}`;

const req = https.get(url, { headers: { "X-API-Key": API_KEY } }, (res) => {
  let data = "";
  res.on("data", (chunk) => (data += chunk));
  res.on("end", () => {
    if (res.statusCode !== 200) {
      console.error(`✗ API error (${res.statusCode}):`, data);
      process.exit(1);
    }
    try {
      const json = JSON.parse(data);
      if (content) {
        console.log(JSON.stringify(json, null, 2));
      } else {
        for (const r of json.results) {
          console.log(`--- Result ${r.position} ---`);
          console.log(`Title: ${r.title}`);
          console.log(`Link: ${r.url}`);
          console.log(`Site: ${r.site_name}`);
          console.log(`Snippet: ${r.snippet}`);
          console.log("");
        }
        console.log(`Total: ${json.total_results} results`);
      }
    } catch (e) {
      console.error("✗ Failed to parse response:", e.message);
      process.exit(1);
    }
  });
});

req.on("error", (e) => {
  console.error("✗ Request failed:", e.message);
  process.exit(1);
});

req.setTimeout(15000, () => {
  req.destroy();
  console.error("✗ Request timed out");
  process.exit(1);
});
