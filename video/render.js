const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const outDir = path.join(__dirname, "out");
fs.mkdirSync(outDir, { recursive: true });

const storyboard = {
  generated_at: new Date().toISOString(),
  scenes: [
    "Board drag/drop and audit event",
    "Create critical alert",
    "Watcher escalation to incident",
    "Audit log + incident timeline",
    "Monitoring dashboard + metrics",
    "Agent remediation tasks",
  ],
};

fs.writeFileSync(path.join(outDir, "storyboard.json"), JSON.stringify(storyboard, null, 2));

try {
  execSync("ffmpeg -version", { stdio: "ignore" });
  const output = path.join(outDir, "demo.mp4");
  const cmd =
    "ffmpeg -y -f lavfi -i color=c=black:s=1280x720:d=8 -vf \"drawtext=text='OpsBoard Demo Placeholder':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2\" " +
    output;
  execSync(cmd, { stdio: "inherit" });
  console.log("Rendered:", output);
} catch (err) {
  console.log("ffmpeg not found; generated storyboard only.");
}
