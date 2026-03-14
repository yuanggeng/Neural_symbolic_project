## Controller training code for the Neural symbolic project.
Here are all the versions for the packages in these codes: 
```
python 3.9; gym 0.26.2; numpy 1.20.3; pytorch 2.1.2+cu121; Pillow 8.3.2
```
We try to train a robust controller with DDPG and MPC.

---

## How to Create an Empty GitHub Repository

Follow these steps to create a new, empty repository on GitHub:

1. **Sign in to GitHub**  
   Go to [https://github.com](https://github.com) and log in to your account.

2. **Start a new repository**  
   Click the **+** icon in the top-right corner of the page and select **New repository**.

3. **Fill in the repository details**  
   - **Repository name**: Enter a unique name for your repository.  
   - **Description** *(optional)*: Add a short description of the project.  
   - **Visibility**: Choose **Public** (visible to everyone) or **Private** (visible only to you and collaborators).

4. **Leave initialization options unchecked**  
   To create a truly empty repository, make sure the following options are **not** selected:
   - Do **not** add a README file.
   - Do **not** add a `.gitignore`.
   - Do **not** choose a license.

5. **Click "Create repository"**  
   GitHub will create the repository and display a quick-setup page with instructions for pushing existing code or cloning the empty repository.

6. **Clone or connect your local project** *(optional)*  
   Use the provided URL to clone the empty repository locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
   ```
   Or connect an existing local project to the new remote:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
   git branch -M main
   git push -u origin main
   ```
