# Publishing this repo (2 minutes)

```bash
# 1. Create the repo on github.com/prateek-ratnakar (public, no README - we have one)
#    Name: personal-agentic-ai-toolkit

# 2. From this folder:
cd personal-agentic-ai-toolkit
git init && git add -A && git commit -m "Initial commit: agentic toolkit - shopping insights, job-search agent, resume pipeline"
git branch -M main
git remote add origin https://github.com/prateek-ratnakar/personal-agentic-ai-toolkit.git
git push -u origin main
```

# Publishing the portfolio (GitHub Pages)

```bash
# 1. Create repo named exactly: prateek-ratnakar.github.io
# 2. Put index.html (from Prateek_Portfolio/) at the repo root:
git init && git add index.html && git commit -m "Portfolio v1"
git branch -M main
git remote add origin https://github.com/prateek-ratnakar/prateek-ratnakar.github.io.git
git push -u origin main
# 3. Live within ~2 min at https://prateek-ratnakar.github.io
# 4. Then add to resume contact line:  | prateek-ratnakar.github.io
```
