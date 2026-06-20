from langchain_community.document_loaders import GitLoader
from rich import print
loader = GitLoader(
    repo_path="./Nexis",
    clone_url="https://github.com/Rahulv1130/Nexis.git",
)

documents = loader.load()
print(documents)

