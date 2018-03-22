Initial Commit as a Proof of Concept but not Implementation.

Note if your cloning the Branch still install the requirements.
1. Install requirements: Requests and Visual Studio Code vs-rest-api extension
Via command prompt
'pip install requests'

Launch VS Code Quick Open (Ctrl+P), paste the following command, and press enter:
ext install vs-rest-api

2. Navigate to your project root folder and look open '.vscode/settings.json' file.

3. The project folder containing "settings.json" with the following contents will automatically lunch the API. Then test out a few commands.
{
    "rest.api": {
        "autoStart": true,
        "openInBrowser": false,
        "port": 1781,
        "guest": {
            "isActive": true,
            "canAnything": true
        },
    }
}

Optionally, open command pallet and type 'REST API' to toggle the API server. 

Documentation on REST API to control your editor. 
https://github.com/mkloubert/vs-rest-api

Eventually, the API server will be moved out of VS extension and restructured to extend to other IDE Rest clients.