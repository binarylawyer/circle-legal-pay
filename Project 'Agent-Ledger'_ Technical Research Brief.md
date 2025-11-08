# **Project 'Agent-Ledger': Technical Research Brief**

## **Section 1: Core Architecture (Path B: Boilerplate-Driven)**

### **1.1. Architectural Mandate**

Our strategy is **Boilerplate-Driven Development**. This is the optimal balance of speed and control for a hackathon. The core principle is to start with a pre-built, functioning application (the "boilerplate") that already provides 90% of the non-core features, such as user accounts, a web server, and database connections. Our task is to surgically *add* our unique 10% of "Agent-Ledger" logic onto this stable foundation.

* **Boilerplate Definition:** Boilerplate code refers to sections of code that can be reused in multiple contexts with little to no modification.\[1, 2, 3, 4, 5\] A "boilerplate starter kit" is a fully functional starter project.\[6\]  
* **Chosen Stack:** We will use a **Python Flask Boilerplate**. Flask is a lightweight and flexible micro-framework, ideal for rapid prototyping and API development.\[7, 8, 9, 10, 11\]  
* **Recommended Boilerplate:** mlh-hackathon-flask-starter.  
  * **Pre-built Features:** This kit already provides user authentication, a project structure, and example routes.  
  * **Setup:** The setup process involves cloning the repo, creating a virtual environment, installing dependencies from requirements.txt, and running the server.

## **Section 2: Hackathon Sponsor Technology (API Integration Guide)**

This section details the specific APIs from the hackathon sponsors and the exact Python implementations required.

### **2.1. Arc Network (Blockchain Layer)**

Arc is the L1 blockchain our application will live on. It is EVM-compatible, which allows us to use standard Python tooling.\[12, 13\]

* **Key Feature:** Arc uses **USDC as the native gas token**.\[12, 14, 15, 16, 17, 18, 19, 20\] This eliminates the need for users to hold a separate volatile gas token and simplifies all transactions.\[21, 15\]  
* **Testnet Details:**  
  * **Network Name:** Arc Testnet \[22\]  
  * **RPC URL:** https://rpc.testnet.arc.network \[22, 23, 24\]  
  * **Chain ID:** 5042002 \[25, 22, 23, 19\]  
  * **Native Currency:** USDC \[25, 22, 15, 23\]  
  * **Testnet Faucet:** Testnet USDC is available from Circle's faucet.\[23, 26, 27\]  
  * **Testnet USDC Address:** 0x3600000000000000000000000000000000000000 (system contract).\[19, 28\]  
* **Python Integration (web3.py):**  
  * **Installation:** pip install web3.  
  * **Connection:** Connect to the Arc Testnet RPC using the standard Web3 provider.  
    Python  
    from web3 import Web3  
    arc\_rpc\_url \= "https://rpc.testnet.arc.network"  
    w3 \= Web3(Web3.HTTPProvider(arc\_rpc\_url))  
    is\_connected \= w3.is\_connected()  
    \# is\_connected will be True

### **2.2. Circle (Wallet & Gas Sponsorship Layer)**

We will use Circle's Wallet-as-a-Service (WaaS) APIs to manage all wallets and sponsor transactions. This is the simplest, fastest, and most powerful integration for our use case.

* **Wallet Model: Developer-Controlled Wallets**  
  * **Definition:** This model allows our Flask backend to retain control over the user's wallet, managing all blockchain interactions (like transfers and contract calls) on their behalf via an API.  
  * **Benefit:** This creates a "gasless" and frictionless user experience, as the user does not need to manage private keys or native gas tokens.  
* **Gas Sponsorship: The "Gas Station"**  
  * **Definition:** Circle's Gas Station is a feature of their wallet platform that allows us, the developer, to sponsor network fees for our users. The sponsored gas fees are then billed to our developer account.  
  * **Benefit:** This is the mechanism that enables "gasless transactions" for our users. When we initiate a transfer from a Developer-Controlled Wallet, we will flag it to be paid by the Gas Station.  
* **Python Integration (Circle SDK):**  
  * **Installation:** pip install circle-sdk. (Note: some docs may show separate packages like circle-user-controlled-wallets or circle-developer-controlled-wallets. We will use the primary circle.web3 utilities).  
  * **Client Initialization:**  
    Python  
    from circle.web3 import utils  
    client \= utils.init\_developer\_controlled\_wallets\_client(  
        api\_key="YOUR\_API\_KEY",  
        entity\_secret="YOUR\_ENTITY\_SECRET"  
    )

  * **Core Functions:** We will wrap this SDK to create wallets, check balances, and initiate gasless transfers.

### **2.3. ElevenLabs (Voice Input/Output Layer)**

We will use ElevenLabs (a sponsor) to provide the "vibe" voice interface for both clients and lawyers.

* **Key Features:**  
  1. **Speech-to-Text (STT):** Transcribe spoken audio into text.  
  2. **Text-to-Speech (TTS):** Convert text into lifelike audio.  
* **Python Integration (ElevenLabs SDK):**  
  * **Installation:** pip install elevenlabs.  
  * **API Key:** Set via environment variable ELEVENLABS\_API\_KEY.  
  * **STT (Voice Input) Example:**  
    Python  
    from elevenlabs.client import ElevenLabs  
    client \= ElevenLabs() \# Reads API key from env  
    audio\_file \= open("path/to/lawyer\_approval.mp3", "rb")

    response \= client.speech\_to\_text.convert(  
        audio=audio\_file  
    )  
    transcript \= response.text  
    \# transcript will be "approve this, case ID 123"

  * **TTS (Voice Output) Example:**  
    Python  
    audio\_bytes \= client.generate(  
        text="Your document has been approved and is in your client locker.",  
        voice="Adam" \# Or any preferred voice ID  
    )  
    \# We can then save this audio\_bytes to a file

## **Section 3: Core Application Logic & Data**

### **3.1. AI Intent Extraction (Gemini/Claude)**

The core of our AI agent is turning unstructured voice commands into structured JSON data that our backend can use.

* **Method:** **Function Calling**. This is the most reliable method for intent extraction. We define a "function" (like approve\_legal\_task) and its required parameters (case\_id, memo), and the AI model (Gemini/Claude) will generate a JSON object matching that function's signature based on the user's text.  
* **Python Integration (Google Gemini):**  
  * **Installation:** pip install google-generativeai  
  * **Example (using Pydantic for structured output):** We can define our desired JSON structure using Pydantic, and the Gemini API can be configured to return data matching that schema.  
    Python  
    import google.generativeai as genai  
    from pydantic import BaseModel, Field

    \# 1\. Define our desired structure  
    class ApproveTask(BaseModel):  
        action: str \= Field(description="The action to take, e.g., 'approve' or 'reject'")  
        case\_id: int \= Field(description="The unique ID for the legal case")  
        memo: str \= Field(description="The lawyer's notes or suggestions")

    \# 2\. Configure the model  
    genai.configure(api\_key="YOUR\_GEMINI\_API\_KEY")  
    model \= genai.GenerativeModel(  
        'gemini-1.5-pro-latest',  
        generation\_config={"response\_mime\_type": "application/json"},  
        system\_instruction="Extract the lawyer's intent into the provided JSON schema."  
    )

    \# 3\. Get transcript from ElevenLabs (see 2.3)  
    transcript \= "This looks good, please approve case 456\. Tell the client I added a clause."

    \# 4\. Prompt the model  
    response \= model.generate\_content(

    )

    \# The 'response.text' will be a JSON string:  
    \# '{"action": "approve", "case\_id": 456, "memo": "Tell the client I added a clause."}'

### **3.2. Legal Service Definitions (The "Platform" Data)**

Our "Legal Service Factory" will be driven by text templates and knowledge of the specific fields required for each legal filing.

* **Task 1: Wyoming DAO LLC** \[29, 30, 31\]  
  * **Required Fields (from Articles of Organization):**  
    1. entity\_name: Must end in "DAO", "LAO", or "DAO LLC".  
    2. registered\_agent\_name: Name of the registered agent in Wyoming.  
    3. registered\_agent\_address: Physical address of the agent.  
    4. dao\_statement: A statement that the entity is a DAO.  
    5. smart\_contract\_identifier: A publicly available identifier of the smart contract used to manage the DAO.  
    6. management\_statement: A statement establishing if management is by members or algorithmic.  
    7. notice\_of\_restrictions: The official "Notice of Restrictions on Duties and Transfers" (or a statement it's in the Operating Agreement).  
* **Task 2: Delaware LLC**  
  * **Required Fields (from Certificate of Formation):**  
    1. entity\_name: Must include "Limited Liability Company", "L.L.C.", or "LLC".  
    2. registered\_agent\_name: Name of the DE Registered Agent.  
    3. registered\_agent\_address: Physical address of the agent in Delaware.  
    4. authorized\_person\_name: Name of the person signing the document.  
* **Task 3: UCC-1 Financing Statement**  
  * **Required Fields:**  
    1. debtor\_name: The exact, full legal name of the debtor.  
    2. secured\_party\_name: The name of the creditor.  
    3. collateral\_description: A description of the collateral covered by the lien.

### **3.3. Client Locker (SharePoint / MS Graph API)**

We will use the Microsoft Graph API to programmatically create folders and upload documents to a SharePoint site.

* **Authentication:** App-only authentication using OAuth 2.0 Client Credentials Flow. This requires registering an app in Azure AD and getting a client\_id, client\_secret, and tenant\_id.  
* **Python Integration (msal \+ requests):**  
  * **Installation:** pip install msal requests  
  * **Step 1: Get Access Token (using msal):**  
    Python  
    import msal

    config \= {  
        "authority": "https://login.microsoftonline.com/YOUR\_TENANT\_ID",  
        "client\_id": "YOUR\_CLIENT\_ID",  
        "client\_secret": "YOUR\_CLIENT\_SECRET",  
        "scope": \["https://graph.microsoft.com/.default"\]  
    }

    app \= msal.ConfidentialClientApplication(  
        config\["client\_id"\],   
        authority=config\["authority"\],  
        client\_credential=config\["client\_secret"\]  
    )

    result \= app.acquire\_token\_for\_client(scopes=config\["scope"\])  
    access\_token \= result\['access\_token'\]

  * **Step 2: Upload File (using requests):**  
    * We need the site-id and drive-id from SharePoint.  
    * The upload URL is: https://graph.microsoft.com/v1.0/sites/{site-id}/drives/{drive-id}/items/root:/{folder\_name}/{file\_name}:/content.

  Python  
      import requests

      headers \= {'Authorization': f'Bearer {access\_token}'}  
      file\_path \= 'path/to/generated\_wy\_dao.txt'  
      file\_name \= 'WY-DAO-Articles.txt'  
      folder\_name \= 'Client\_Locker\_Case\_456'

      with open(file\_path, 'rb') as file\_data:  
          response \= requests.put(  
              f"https://graph.microsoft.com/v1.0/sites/{site\_id}/drives/{drive\_id}/items/root:/{folder\_name}/{file\_name}:/content",  
              headers=headers,  
              data=file\_data  
          )  
      \# response.status\_code \== 201 means success

  * **Step 3: Manage Permissions:** We can use other Graph API endpoints to modify the sharing settings of the uploaded file (e.g., make it read-only, grant access to the client's email).

## **Section 4: Hackathon Strategy & Pitch**

* **Judging Criteria:** Submissions are judged on "Application of Technology," "Business Value," and "Originality".\[32\]  
* **A-to-Z Demo:** The pitch must show a complete, end-to-end user flow, not just isolated features.\[33\]  
* **Pitch Structure (3 Minutes):** \[34, 35\]  
  1. **Intro (10s):** Team.  
  2. **Problem (20s):** Legal services are slow, expensive, and opaque. AI agents and DAOs have no way to interact with the real-world legal system.  
  3. **Product/Demo (1m 30s):** This is the live demo. We will show the 10-step flow:  
     * Show the web form (Step B).  
     * Show the "Vibe Coder" API, using ElevenLabs to send a voice command (Step B, alt).  
     * Show the lawyer's simple "approve" audio file (Step E).  
     * Show the final document in the SharePoint "Client Locker" (Step F).  
     * Show the Arc Testnet explorer, proving the USDC transfer from "escrow" to "law firm" wallet, sponsored by the Circle Gas Station (Step H).  
  4. **The "Platform" Vision (30s):** Explain that this isn't just for one form. It's a *platform* (the "Legal Service Factory") for any deterministic legal task, showing the slide with the WY DAO, DE LLC, and UCC-1 logos.\[33, 36, 37\]  
  5. **Wrap-up (30s):** Reiterate the core value: We are building the on-chain RWA layer for legal services, powered by Arc, Circle, and AI.