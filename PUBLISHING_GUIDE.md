# Publishing Guide for Memorial PDF Generator

## Step-by-Step Process to Publish Your Project

### **Phase 1: Prepare Your GitHub Repository**

#### Step 1: Verify Repository Visibility
1. Go to your GitHub repository: `https://github.com/[your-username]/memorial-pdf-generator`
2. Click **Settings** → **General**
3. Under "Danger Zone", ensure the repository is **Public** (not Private)
4. Click **Save**

#### Step 2: Create a LICENSE File
1. In your repository root, create a file named `LICENSE`
2. Copy the full GPLv3 license text from: https://www.gnu.org/licenses/gpl-3.0.txt
3. Commit and push:
   ```bash
   git add LICENSE
   git commit -m "Add GPLv3 LICENSE file"
   git push origin main
   ```

#### Step 3: Add Repository Description & Topics
1. Go to your repository homepage
2. Click the **Settings** icon (gear) next to "About"
3. Add:
   - **Description**: "Create elegant memorial PDFs with poems and photos using Flask"
   - **Website**: (Leave empty for now, unless you have a deployed version)
   - **Topics**: Add these tags:
     - `memorial`
     - `pdf-generator`
     - `flask`
     - `python`
     - `poetry`
     - `tribute`
4. Click **Save changes**

#### Step 4: Add a .gitignore File
Create `.gitignore` in your root directory:

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
temp/
```

Commit it:
```bash
git add .gitignore
git commit -m "Add .gitignore file"
git push origin main
```

---

### **Phase 2: Enhance Project Documentation**

#### Step 5: Create CONTRIBUTING.md
Create `CONTRIBUTING.md`:

```markdown
# Contributing to Memorial PDF Generator

Thank you for your interest in contributing!

## How to Contribute

1. **Fork the repository** on GitHub
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and test them
4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: description of your change"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a Pull Request** with a clear description

## Code Style

- Follow PEP 8 for Python code
- Add docstrings to functions
- Comment complex logic
- Test your changes

## Reporting Issues

Use GitHub Issues to report bugs. Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and OS
```

Commit it:
```bash
git add CONTRIBUTING.md
git commit -m "Add CONTRIBUTING.md"
git push origin main
```

#### Step 6: Create CHANGELOG.md
Create `CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-05-23

### Added
- Initial release of Memorial PDF Generator
- Web interface for creating memorial PDFs
- Support for custom titles, poems, dates, and author names
- Photo upload functionality (JPG, PNG, GIF, WebP)
- Auto-detect and manual column layout options
- Beautiful dark theme with gold accents
- Flask-based web application
- Comprehensive documentation and README

### Features
- Create elegant memorial PDFs
- Customizable layouts
- Easy-to-use web interface
- GPL v3 licensed

## [Future]

### Planned Features
- Email PDF directly
- Template themes
- Multi-language support
- Social media sharing
```

Commit it:
```bash
git add CHANGELOG.md
git commit -m "Add CHANGELOG.md"
git push origin main
```

---

### **Phase 3: Create Release & Version Tags**

#### Step 7: Create a Release on GitHub
1. Go to your repository
2. Click **Releases** in the right sidebar
3. Click **Create a new release**
4. Fill in:
   - **Tag version**: `v1.0.0`
   - **Release title**: `Memorial PDF Generator v1.0.0`
   - **Description**:
     ```
     ## Initial Release

     Memorial PDF Generator is now available!

     ### Features
     - Create beautiful memorial PDFs with poems and photos
     - Web-based interface with drag-and-drop support
     - Customizable layouts (single or two-column)
     - Support for multiple image formats
     - Author attribution
     - Elegant dark theme

     ### Installation
     ```bash
     git clone https://github.com/[your-username]/memorial-pdf-generator.git
     pip install -r requirements.txt
     python app.py
     ```

     ### License
     Licensed under GPLv3 - see LICENSE file for details

     ### Author
     Created by Agalya
     ```
5. Check **"This is a pre-release"** if still in development
6. Click **Publish release**

---

### **Phase 4: Deploy Your Web Application (Optional)**

#### Step 8: Choose a Hosting Platform

**Option A: Deploy to Heroku (Free tier available)**

1. Sign up at https://www.heroku.com/
2. Install Heroku CLI
3. Create `Procfile` in your root:
   ```
   web: python app.py
   ```
4. Create `runtime.txt`:
   ```
   python-3.11.0
   ```
5. Commit these files:
   ```bash
   git add Procfile runtime.txt
   git commit -m "Add Heroku deployment configuration"
   git push origin main
   ```
6. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

**Option B: Deploy to PythonAnywhere**

1. Sign up at https://www.pythonanywhere.com/
2. Upload your files via their web interface
3. Configure a Flask web app
4. Your app will be live at `yourusername.pythonanywhere.com`

**Option C: Deploy to AWS/Google Cloud/Azure**

Follow platform-specific documentation for Flask deployment.

---

### **Phase 5: Promote Your Project**

#### Step 9: Share on Social Media & Communities

**GitHub Platforms:**
- Add to GitHub trending by getting stars: Share with friends and communities
- GitHub Topics: Already added in Step 3
- GitHub Discussions: Enable in repository settings

**Development Communities:**
1. **Reddit**:
   - r/Python
   - r/Flask
   - r/webdev
   - r/programming

2. **Twitter/X**:
   ```
   🎉 Just published Memorial PDF Generator! 
   Create elegant memorial PDFs with poems & photos
   Built with Flask & Python
   Open source (GPLv3)
   https://github.com/your-username/memorial-pdf-generator
   #OpenSource #Python #Flask #GitHub
   ```

3. **Dev.to**:
   - Write a blog post about your project
   - Share on https://dev.to/

4. **Product Hunt**:
   - Submit at https://www.producthunt.com/
   - Good for getting visibility

5. **Hacker News**:
   - Submit to https://news.ycombinator.com/

#### Step 10: Create a Project Website (Optional)

Use GitHub Pages:

1. Create `gh-pages` branch:
   ```bash
   git checkout --orphan gh-pages
   git reset --hard
   ```

2. Create `index.html` with project info:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <title>Memorial PDF Generator</title>
       <meta name="description" content="Create elegant memorial PDFs with poems and photos">
   </head>
   <body>
       <h1>Memorial PDF Generator</h1>
       <p>Create beautiful memorials with your poems and photos</p>
       <a href="https://github.com/your-username/memorial-pdf-generator">View on GitHub</a>
       <a href="[deployed-url]">Try Live Demo</a>
   </body>
   </html>
   ```

3. Push:
   ```bash
   git add index.html
   git commit -m "Add GitHub Pages"
   git push origin gh-pages
   ```

4. Enable in repository Settings → Pages → Source: gh-pages branch

---

### **Phase 6: Maintain & Update**

#### Step 11: Set Up Continuous Integration (CI)

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest
```

#### Step 12: Regular Maintenance

- Monitor GitHub Issues
- Review Pull Requests
- Update dependencies monthly
- Keep CHANGELOG.md updated
- Respond to users

---

## Summary Checklist

- [ ] Repository is Public
- [ ] LICENSE file added
- [ ] README.md complete
- [ ] CONTRIBUTING.md created
- [ ] CHANGELOG.md created
- [ ] Repository description and topics added
- [ ] .gitignore in place
- [ ] First release created (v1.0.0)
- [ ] Project deployed (optional)
- [ ] Shared on social media
- [ ] GitHub Pages setup (optional)
- [ ] CI/CD configured (optional)

## Result

Your project will be:
- ✅ Publicly available on GitHub
- ✅ Easily discoverable
- ✅ Well-documented
- ✅ Professional-looking
- ✅ Ready for contributions
- ✅ Live online (if deployed)

---

**Questions?** Check GitHub documentation or reach out to the community!
