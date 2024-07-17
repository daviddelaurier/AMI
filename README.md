   # A.M.I.
   Artificial Me Intelligence

![myAI](https://i.imgur.com/GXpjcgB.png)

## Cameras and Microphones Are All You Need

## WARNING

I believe that AI systems must be fully integrated into your environment to truly enhance its users. 
This causes issues when building ML and LLMs into products because you must violate all privacy of the user.

Realizing this, I have decided to build it myself. Anyone is welcome to try this for themselves obviously, but dont come crying to me when your entire life is used as training data for GPT-5. 

USE AT YOUR OWN RISK!

## Initial Implementations (more to come)

### Business desk:
   - Automatic OCR when documents are placed in the "IN" Document Bin
   - Keep track of what I was previously working on because I never remember and no app exists that does this well.

### Ceramic 3D printer:
   - Natural language to 3d printed object.
   - Monitor the success or failure of prints.
   - Log Glaze Reicpies
   - Log Kiln Settings
   - Log Weather Data during firing process

### Plotting Robot:
   - Natural language to SVG text/image that is routed to the robot.
   - Ask my AI write personalized thank you letters to clients using the pen plotter.
   - Ask my AI to create drawing mockups for new project ideas I am working on.

### Office kitchen:
   - Monitor the contents of my refrigerator and tell me what to make based on available ingredients, previous meals, and expiration dates.
   - Tell me when it's time to load the dishes into the dishwasher.
   - Tell me when the dishwasher cycle is complete.
   - Monitor my coffee consumption and the amount of coffee left in the pot.

### Backyard and parking area:
   - Monitor my two dogs' activities to ensure their well-being and safety.
   - Track both of my vehicle usages for maintenance and scheduling.
   - Tell me to take the trash out on the designated day and time.
   - Tell me if someone other than me or my wife are in the backyard or parking area.

## Stack

### Machine Learning
- moondream2
- Florence-2
- Sonnet 3.5
- MARS5(TBD)
- Whisper-v3
- Text-to CAD
- Porcupine

### LLMs
llama-3-70B
llama-3-8B
claude-sonnet-long-context

### ???
- Robotic control for the pen plotting robot

### OBS Overlays (dont need API's...)
- Scheduling and reminder system via screencapture/VLM request of all datastreams I am interested in.

## Expanded Uses and Long-term Analysis

Capabilities extend beyond daily tasks and can provide valuable insights through long-term data analysis. 
By continuously monitoring various aspects of your life and work, 
identify patterns, optimize processes, and help you make informed decisions.

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

<<<<<<< HEAD
# Contact Information

    David DeLaurier
    
    Twitter:    @DataDeLaurier
    
    eMail:      DataDeLaurier@gmail.com
    
        www.pdf2search.com      www.text2ceramic.com
   
   ---

   Copyright 2024 David DeLaurier, pdf2search, LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
=======
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



>>>>>>> f7485dce7bd638046bb60b55ee6e08671868c23e
