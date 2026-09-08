# Setup

This ZIP is configured for `github.com/sudeenjain/sudeenjain`.

## 1. Keep your existing resume.pdf

Your current repository already has `resume.pdf`.
This ZIP does not include a replacement PDF, so keep that existing file in the repository root.

Final root:

```text
README.md
resume.pdf
SETUP.md
assets/
scripts/
.github/
```

## 2. Upload

Recommended on a computer:

```bash
git clone https://github.com/sudeenjain/sudeenjain.git
cd sudeenjain
```

Extract this ZIP and copy its contents into the cloned repository.
Do not delete `resume.pdf`.

Then:

```bash
git add .
git commit -m "upgrade GitHub profile"
git push
```

## 3. Give Actions write permission

Repository → Settings → Actions → General → Workflow permissions →
select **Read and write permissions** → Save.

## 4. Add METRICS_TOKEN

For the 3D calendar and advanced metrics:

GitHub Settings → Developer settings → Personal access tokens →
Generate token (classic) with `read:user`.

Then your profile repository →
Settings → Secrets and variables → Actions → New repository secret.

Name:

```text
METRICS_TOKEN
```

Paste the token and save.

## 5. Run once

Actions tab → manually run:

1. Generate contribution snake
2. Refresh profile charts
3. Refresh GitHub metrics

After that, the workflows refresh automatically.

## Customize

- Portrait: `assets/profile/portrait.png`
- Skill levels: `assets/skills.json`
- Featured projects: `assets/projects.json`
- Main content: `README.md`
