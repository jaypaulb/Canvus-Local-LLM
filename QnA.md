# PRD Development Questions & Answers

## 1. Architecture & Deployment
**Question:** Should this be a standalone desktop application, a web service, or a command-line tool? What's the preferred user interface?

**Answer:**
Stand alone tool that sits in the app tray by the clock in windows.
Right click options are
    - Restart
    - Settings
      - Set Canvus Server Address
      - Set API Key 
      - Set Username (Optional not shown if API Key set)
      - Set Password (Optional not shown if API Key set)
---

## 2. Real-time Processing
**Question:** How frequently should the system poll Canvus workspaces for new content? (e.g., every 30 seconds, every 5 minutes, or event-driven?)

**Answer:**
The app will leverage the "?subscribe" function detailed in [text](<Docs/Canvus API Docs/Canvases_API.md>) 
Essential this appends ?subscribe to the api get call to MTCS and MTCS then responds with a ascii text data stream with one line per update - each line is a json object as text and will need to be parsed as json before processing.
A blank line is sent as a keep alive in the event on no changes so this should be managed in the app.

Ideally we would have a staged processing for subscribing.
1. sub to clients endpoint.
   1. On new client get workspaces.
   2. Iterate over workspaces to get the CanvasID's open on that client.
   3. Start a seperate process to Sub to that \canvases\canvasid\ endpoint to monitor all updates on that canvas.
---

## 3. Content Detection
**Question:** Should the system only process content within `{{ }}` braces, or do you want additional trigger mechanisms (like specific widget types, keywords, or file uploads)?

**Answer:**
We need to trigger on a number of differnt elements based on the use case.  Each of these has its own workflow.
## Usage

1. **Basic AI Interaction**:
   - Create a note in your Canvus workspace
   - Type your prompt inside double curly braces: `{{What is the capital of France?}}`
   - The system will process the prompt and create a new note with the AI response
- If the monitor of the canvus sees a Note that matches the begins and ends with '{{}}' it should trigger.
- It should remove the {{ }} from the triggering note - update it to indicate that it is processing the note to the AI and then send the text to the LLM for processing.  There should be some system Prompt to the LLM to indicate the task.

1. **PDF Analysis**:
   - Upload a PDF to your canvas
   - Place the AI_Icon_PDF_Precis on the PDF
   - The system will analyze and summarize the PDF content
- If the monitor sees that an image with the title AI_Icon_PDF_Precis it should get the Widget with the ID = ParentID of the icon.  If that is a PDF widget_type it should trigger.
- Trigger means download the PDF from Canvus Server, process it to extract the text, chuck the text in such a way that it can be processed to the LLM based on the token limit set in the settings file and then process the text to the LLM to create a Precis of that PDF's content.

1. **Canvas Analysis**:
   - Place the AI_Icon_Canvus_Precis on your canvas
   - The system will analyze all content and relationships between items
   - Receive an overview and insights about your workspace
- This works in a very similar way to the PDF Precis above. If the AI_Icon_Canvus_Precis ParentID = the BackgroundID then we trigger.
- Trigger means that we GET widgets for the whole canvas with annotatoins (see [text](<Docs/Canvus API Docs>)) and we pass that whole data set to the LLM for analysis to great a summary.  There will be some system prompt to steer the LLM in the right direction on this.

1. **Image Generation**: (Later Phase since Ollama has no ImageGen Native support)
   - Include an image generation prompt in your note: `{{Generate an image of a sunset}}`
   - The system will create and place the generated image on your canvas
- This will be the same as the note response -  we need the system prompt for the note input to ensure that the LLM can make this decision and respond with a json object indicating if its a Widget_type: "Note" or Widget_type: "Image".  For an LLM Image Gen prompt should be the text: element that we can then extract and pass in the method needed for imagegen as a second llm process to a alternate platform.
---

1. **Snapshot Analysis**: 
   - Take Snapshot of a widget or onscreen ink to convert this to a note with editable text.
   - The system will create a note in the same location and size as the snapshot with the text extracted and delete the snapshot.
- If an image is created with the Title: "Snapshot at ..." this should trigger the Snapshot process.
- This trigger downloads the image to a local file, creates a feedback note to explain what is happening to the user, then passes that file to the LLM for analysis, replacing the feedback note with the response note from the llm.  
---

## 4. AI Model Selection
**Question:** Which Ollama models should be supported by default? Should users be able to configure different models for different types of tasks?

**Answer:**
Only vision models can be supported.
https://ollama.com/search?c=vision lists these models 
I guess we can add a settings to the icon to select the model with the default always being Gemma3
---

## 5. Multimodal Capabilities
**Question:** For the image generation feature, should the system use a specific image generation model (like Stable Diffusion), or should it leverage multimodal models that can generate images from text?

**Answer:**
If there is a simple way to do this with StableDiffusion that is not going to require significant processes to setup we can do that but lets get everything else working first.
For now lets just populate a note with the expanded image prompt from Ollama in the note.
---

## 6. PDF Processing
**Question:** Should PDF analysis be limited to text extraction and summarization, or do you want OCR capabilities for scanned documents as well?

**Answer:**
We need to use PDFium or something to extract the text before processing it into chunks to pass to the LLM for processing into a precis.  More details are in [text](Docs/Summarizing_long_documents.ipynb)
---

## 7. Canvas Analysis Scope
**Question:** When analyzing canvas content, should the system consider all widgets (notes, images, PDFs, videos, browsers) or focus on specific types?

**Answer:**
All widgets including connectors as these provide context on what led to what.  Also Anchor widgets should be used to determine what "area" of the canvus the items belong too.  For example if there a lots of notes withing the area covered by the Brainstorm anchor it can be assumed that these notes were a brainstorming session.  If items are in the Outcomes zone then they are likely determined outcomes for the meeting, etc etc.
---

## 8. Response Placement
**Question:** Where should AI responses be placed? In the same note, as a new note, or as a separate widget type?

**Answer:**
A new note the same colour, location as the old note.
However with the Alpha Channel set to 66% so as to see the triggering widget below it.
We need to do some clever math here to determine the Scale and Size of the new note such that it fills the same area as the old note.  This needs to work out the number of characters in the response and then adjust the size of the note to accommodate the total number of characters.  Once we have the new size we need to change the scale so that it will appear the same onscreen as the old note.
We will likely need to do some testing here.
This is the text that fits in a single standard note
"123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"
---

## 9. Error Handling & Retry
**Question:** What should happen when AI processing fails? Should there be automatic retries, and how should failed operations be communicated to users?

**Answer:**
yes three retries, immidately, 10s, 30s.  The trigger note or feedback note for PDF/Canvus/Snapshot analysis should be updated to indicated that we are counting down a wait to retry and the error message.
---

## 10. Security & Authentication
**Question:** How should the system handle Canvus authentication? Should it support both API key and username/password methods?

**Answer:**
Both with API Key preferred.
---

## 11. Configuration Management
**Question:** Should configuration be stored in a local file, environment variables, or a combination? What settings should be user-configurable?

**Answer:**
I defined this above.  The full settings should be stored in a local file, editing them from the right click menu in the system tray icon.
---

## 12. Logging & Monitoring
**Question:** What level of logging detail is needed? Should there be a user interface for viewing logs, or just file-based logging?

**Answer:**
logs should be saved the the .log file.  There should be a --debug option to start the process in debug mode for comprehensive logging with normal logging on by default.
---

## 13. Performance & Resource Usage
**Question:** Are there any constraints on CPU/memory usage, or should the system use whatever resources are available?

**Answer:**
No constraints but we should write this to be as memory and CPU optimal as we can since this will run in the background whilst the foreground user apps are being used.
---

## 14. Concurrent Processing
**Question:** Should the system process multiple requests simultaneously, or queue them sequentially?

**Answer:**
Each trigger should not block other triggers from processing.
---

## 15. Model Management
**Question:** Should the system automatically download required Ollama models, or require manual installation?

**Answer:**
Automatically if not downloaded already.
---

## 16. Integration Points
**Question:** Should this integrate with any other systems (like file systems, databases, or external APIs) beyond Canvus and Ollama?

**Answer:**
No.
---

## 17. User Experience
**Question:** Should there be visual indicators (like color-coded notes) to show processing status? What feedback should users get?

**Answer:**
Yes feedback notes indicating what stage of the process we are at would be great.  We can use a traffic light system and patch the note as we progress, we can also patch the text with details.
---

## 18. Data Persistence
**Question:** Should the system maintain any local state or history of processed requests? For how long?

**Answer:**
I don't think this is needed.  We need to take care that we are not processing a trigger multiple times though.  for example we are only really intersested in changes to Title, Text, ParentID.  We don't really care about monitoring for changes to any other aspect of the note.  We need to know those aspects once we start processing the note but for the trigger only these core elements for a diff need to be checked.
We need to be carefull we don't miss the creation of a new widget, but also that moving the widget as it is triggering doesnt create a race condition where we attempt to process it multiple times as MTCS will send a valid triggering update for each pixel moved!
The ?subcribe function to the canvas can be a firehose of updates.
---

## 19. Scalability
**Question:** Should the system support multiple Canvus servers or multiple Ollama instances?

**Answer:**
No.
---

## 20. Development & Testing
**Question:** What's the preferred development environment and testing approach? Should there be unit tests, integration tests, or both?

**Answer:**
I have no idea how to answer this, I'm not a developer I just vibe code.
---
