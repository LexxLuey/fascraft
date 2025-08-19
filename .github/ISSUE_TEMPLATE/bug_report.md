---
name: 🐛 Bug Report
about: Create a report to help us improve FasCraft
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''
---

## 🐛 **Bug Description**

**A clear and concise description of what the bug is.**

---

## 🔄 **Steps to Reproduce**

1. **Command executed:**
   ```bash
   # Replace with your actual command
   poetry run fascraft new my-project
   ```

2. **What happened:**
   ```bash
   # Replace with actual error output
   ❌ Error: Something went wrong
   ```

3. **Expected behavior:**
   ```bash
   # What should have happened instead
   ✅ Project created successfully
   ```

---

## 📋 **Environment Information**

### **System Details**
- **Operating System:** [e.g., Windows 11, macOS 13.0, Ubuntu 22.04]
- **Python Version:** [e.g., 3.10.0, 3.11.5]
- **FasCraft Version:** [e.g., 0.4.0, 0.5.0-beta]
- **Installation Method:** [e.g., pip, poetry, source]

### **Dependencies**
```bash
# Run this and paste the output
poetry show --tree
# or
pip list
```

### **Virtual Environment**
- [ ] Using virtual environment
- [ ] Using Poetry
- [ ] Using pip directly
- [ ] Using system Python

---

## 🚨 **Error Details**

### **Full Error Message**
```bash
# Paste the complete error message here
Traceback (most recent call last):
  File "...", line ..., in ...
    ...
Error: Something went wrong
```

### **Error Location**
- **File:** [e.g., fascraft/commands/new.py]
- **Line Number:** [e.g., 42]
- **Function:** [e.g., create_new_project]

---

## 🔍 **Additional Context**

### **What were you trying to do?**
[Describe your goal and what you were trying to accomplish]

### **When did this start happening?**
- [ ] First time using FasCraft
- [ ] After updating FasCraft
- [ ] After changing system configuration
- [ ] After installing new dependencies
- [ ] Other: [Please describe]

### **Can you reproduce this consistently?**
- [ ] Yes, every time
- [ ] Sometimes (describe when)
- [ ] No, it's intermittent
- [ ] Only under specific conditions

---

## 📁 **Project Information** (if applicable)

### **Project Structure**
```bash
# If the bug occurred during project creation, what was the intended structure?
# If the bug occurred in an existing project, show the current structure
tree -L 3
# or
dir /s
```

### **Configuration Files**
```toml
# If relevant, show your fascraft.toml or other config files
[tool.fascraft]
# ... your configuration
```

---

## 🧪 **Troubleshooting Attempts**

### **What have you already tried?**
- [ ] Checked the [troubleshooting guide](docs/troubleshooting.md)
- [ ] Searched existing [GitHub issues](https://github.com/LexxLuey/fascraft/issues)
- [ ] Reinstalled FasCraft
- [ ] Cleared template cache
- [ ] Used different Python version
- [ ] Used different installation method
- [ ] Other: [Please describe]

### **Results of troubleshooting:**
[Describe what happened when you tried each solution]

---

## 📸 **Screenshots/Logs**

### **Screenshots**
If applicable, add screenshots to help explain your problem.

### **Logs**
```bash
# If you have debug logs, paste them here
export FASCRAFT_DEBUG=1
poetry run fascraft new my-project
```

---

## 💡 **Additional Information**

### **Related Issues**
- [ ] I have searched existing issues and found no duplicates
- [ ] This issue is related to [issue number]
- [ ] This issue is blocking [describe what you can't do]

### **Priority**
- [ ] **Critical** - Completely blocks my workflow
- [ ] **High** - Significantly impacts my productivity
- [ ] **Medium** - Annoying but workable
- [ ] **Low** - Minor inconvenience

### **Workaround**
[If you found a temporary workaround, describe it here]

---

## 🔧 **Technical Details** (for developers)

### **Stack Trace Analysis**
[If you can analyze the stack trace, provide insights]

### **Reproduction Environment**
[Describe your exact environment setup]

### **Related Components**
[List any related FasCraft components or dependencies]

---

## 📝 **Checklist**

Before submitting this bug report, please ensure:

- [ ] I have provided all required information
- [ ] I have searched existing issues for duplicates
- [ ] I have checked the troubleshooting guide
- [ ] I have tested with a clean environment
- [ ] I can reproduce the issue consistently
- [ ] I have provided clear steps to reproduce
- [ ] I have included relevant error messages and logs

---

## 🆘 **Need Immediate Help?**

If this is a critical issue blocking your work:

1. **Join our Discord**: [Get real-time help](https://discord.gg/fascraft)
2. **Check GitHub Discussions**: [Community support](https://github.com/LexxLuey/fascraft/discussions)
3. **Review Examples**: [Working examples](../examples/)

---

**Thank you for helping improve FasCraft! 🚀**

Your detailed bug report helps us identify and fix issues faster, making FasCraft better for everyone.
