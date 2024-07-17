

![myAI](https://i.imgur.com/GXpjcgB.png)


# myAI: Seamless AI Integration for Enhanced Living

## Embracing the Future of AI-Assisted Environments

In an era where artificial intelligence is rapidly evolving, myAI stands at the forefront of integrating cutting-edge AI technologies into our daily lives. This project aims to create a fully immersive AI-assisted environment that enhances productivity, creativity, and overall quality of life.

## A Note on Privacy and Data Usage

It's important to acknowledge that the comprehensive nature of myAI's integration raises significant privacy considerations. By design, this system requires access to various aspects of your environment to function optimally. Users should be aware that this level of integration means that a substantial amount of personal data will be processed and analyzed by the AI.

**IMPORTANT:** This project is intended for personal use and experimentation. By implementing myAI, you are choosing to prioritize the benefits of a fully integrated AI assistant over traditional notions of privacy. Please consider the implications carefully before proceeding.

## Key Features and Implementations

myAI is designed to seamlessly integrate into various aspects of your home and work environment. Here are some of the initial implementations:

1. **Business Desk Optimization**
   - Automatic OCR for document processing
   - Intelligent task tracking and work resumption assistance

2. **Ceramic 3D Printing Assistant**
   - Natural language to 3D object conversion
   - Print monitoring and analysis
   - Glaze recipe and kiln setting management
   - Weather data logging for firing processes

3. **Artistic Collaboration with Plotting Robot**
   - Natural language to SVG conversion for robotic plotting
   - AI-generated personalized thank-you letters
   - Collaborative mockup creation for new projects

4. **Smart Kitchen Management**
   - Intelligent recipe suggestions based on available ingredients
   - Automated dishwasher cycle notifications
   - Coffee consumption tracking and analysis

5. **Home Environment Monitoring**
   - Pet activity and well-being tracking
   - Vehicle usage monitoring for maintenance scheduling
   - Automated reminders for household tasks
   - Security monitoring for unauthorized presence

## Technology Stack

myAI leverages a powerful combination of machine learning models, language models, and specialized AI tools to deliver its wide range of functionalities. Some key components include:

- **Machine Learning:** moondream2, Florence-2, Sonnet 3.5, MARS5 (TBD), Whisper-v3
- **Language Models:** llama-3-70B, llama-3-8B, claude-sonnet-long-context
- **Specialized Tools:** Text-to-CAD, Porcupine

Join us in exploring the possibilities of a fully AI-integrated lifestyle with myAI. The future of smart living starts here.

## Expanded Uses and Long-term Analysis

myAI's capabilities extend beyond daily tasks and can provide valuable insights through long-term data analysis. By continuously monitoring various aspects of your life and work, myAI can identify patterns, optimize processes, and help you make informed decisions. Some expanded uses include:

1. **Productivity Analysis**
   - Track the time spent on different tasks and projects
   - Identify productivity patterns and suggest improvements
   - Monitor progress towards long-term goals and deadlines

2. **3D Printing Optimization**
   - Analyze the success rate of prints over time
   - Identify common issues and suggest preventive measures
   - Optimize print settings based on historical data

3. **Pen Plotting Art Evolution**
   - Track the progression of your pen plotting art style
   - Identify popular designs and themes based on client feedback
   - Suggest new design ideas based on previous successful projects

4. **Coffee Consumption Insights**
   - Analyze coffee consumption patterns over time
   - Identify factors influencing coffee intake (e.g., workload, stress)
   - Suggest optimal coffee consumption for productivity and well-being

5. **Kitchen Inventory Management**
   - Track the usage of ingredients over time
   - Predict when certain items will run out and suggest restocking
   - Identify rarely used items and suggest recipes to minimize waste

6. **Pet Behavior Analysis**
   - Monitor changes in your dogs' behavior and activity levels
   - Identify potential health issues or behavioral changes
   - Suggest adjustments to pet care routines based on insights

7. **Vehicle Maintenance Scheduling**
   - Track vehicle usage and maintenance history
   - Predict when certain maintenance tasks will be required
   - Suggest optimal times for scheduling maintenance appointments

# TODO

### Version 0.0.2

# Table of Contents

1. [Completed](#completed)
2. [Source Code](#source-code)
3. [Front End](#front-end)
4. [Back End](#back-end)
5. [Database](#database)
6. [Data Capture and Management](#data-capture-and-management)
7. [General Tasks](#general-tasks)

## Completed
- [x] Setting up project structure
- [x] Implementing core functionality
- [x] Set up version control
- [x] Create project structure and directories
- [x] Create input components for user text/audio
- [x] Add output components for responses and synthesized speech
- [x] Install Hardware
  - [ ] Cameras
    - [x] Office
      - [x] Desktop (Webcam)
      - [x] Office Wide Angle (iPad)
      - [x] Pen Plotting Robot (iPhone)
      - [x] 3D Printer (iPhone)
      - [x] Desk (top-down)
    - [x] Backyard/Parking
      - [x] CCTV
    - [x] Vehicle
      - [x] Dashcam (iPhone)
      - [x] Interior (iPhone)
      - [ ] Exterior (insta360)
  - [x] Microphones
    - [x] Office Microphone
    - [ ] Backyard Microphone
    - [ ] Parking Area Microphone
    - [x] Vehicle Microphone
    - [x] Vanity Microphone
  - [x] Sensors
    - [x] Office
      - [x] Temperature
      - [x] Humidity
      - [x] AQI
    - [x] Backyard
      - [x] Temperature
      - [x] Humidity
      - [x] AQI
    - [x] Vehicle
      - [x] OBD-II

- [x] Setup media storage system
- [x] Connect 3D printer and pen plotting robot to the system
- [ ] Integrate object detection and tracking model
- [x] Implement text-to-3D model conversion system
- [x] Set up natural language processing for request understanding and response generation
- [ ] Configure robotic control system for pen plotting robot
- [ ] Customize scheduling and reminder systems
- [ ] Implement business desk monitoring and task tracking
- [ ] Enable 3D printer control and print monitoring
- [ ] Develop pen plotting robot control and letter writing functionality
- [ ] Set up coffee pot monitoring and consumption tracking
- [ ] Implement office kitchen monitoring and recipe suggestion
- [ ] Enable backyard and parking area surveillance and reminders
- [ ] Implement productivity analysis and insights
- [ ] Design logo
- [ ] Create color palette

## Source Code
- [ ] Implement error handling and logging system
- [ ] Write unit tests for core functionalities
- [ ] Set up continuous integration/continuous deployment (CI/CD) pipeline
- [ ] Implement file upload for images
- [ ] Enhance UI with custom styling
- [ ] Add progress bars or loading indicators for API processes
- [ ] Implement chat history display

## Front End

### Gradio UI
- [ ] Implement chat history display
- [ ] Add file upload for images
- [ ] Enhance UI with custom styling
- [ ] Add progress bars or loading indicators for API processes

### Brand Art
- [ ] Design icons for UI elements
- [ ] Create additional brand assets (e.g., social media banners, documentation templates)

## Back End

### Core Functionality
- [ ] Implement user authentication system
- [ ] Develop chat history saving functionality

### User Management
- [ ] Create user registration and login handlers
- [ ] Implement secure password hashing and storage
- [ ] Develop user profile management system

### Chat History
- [ ] Implement chat history storage mechanism
- [ ] Create chat history retrieval functionality
- [ ] Develop chat history search feature
- [ ] Create chat history export functionality

## Database

### Schema Design
- [ ] Design database schema for API call tracking with columns:
  - system_message
  - user_message
  - transcription
  - image_filename
  - image_data (base64)
  - user_audio_filename
  - synthesized_audio_filename
- [ ] Design database schema for user accounts
- [ ] Design database schema for chat history

### Implementation
- [ ] Set up SQLite database
- [ ] Implement database connection and management in the application
- [ ] Create database migration scripts

## Data Capture and Management

### OBS Studio Integration
- [x] Set up OBS Studio with NDI for video streaming
  - Install OBS Studio and NDI plugin
  - Configure NDI output in OBS settings
  - Test NDI stream with a receiver application
- [x] Integrate OBS Python SDK into the project
  - Install OBS Python SDK
  - Set up project structure to include OBS scripts
- [x] Implement basic OBS control functions (start/stop streaming, switch scenes, etc.)
- [ ] Implement advanced OBS features
- [ ] Error handling and logging for OBS operations

### AI and Machine Learning
- [ ] Develop 3D printing optimization based on historical data
- [ ] Track pen plotting art evolution and suggest new design ideas
- [ ] Provide coffee consumption insights and recommendations
- [ ] Enable kitchen inventory management and waste reduction
- [ ] Implement pet behavior analysis and care suggestions
- [ ] Set up vehicle maintenance scheduling and predictions



