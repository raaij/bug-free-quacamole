# DrawDash: Frontend Requirements

## Key Insights
- Users expect **instant feedback** during processing
- **Split-screen** layouts work well for iterative refinement (input/output)
- **Progress indicators** reduce anxiety during AI processing
- **Chat interfaces** feel natural for iterative improvements
- **Visual upload zones** with drag-and-drop improve UX

## User Flow

```
Screen 1: Upload Screen
    |
  [User uploads dataset, screenshot, adds optional text]
    |
  [Clicks "Upload" button]
    |
  [Button transforms into progress bar inline]
    |
  [Shows: "Uploading data to DuckDB..." � "Understanding your requirements..."]
    |
  [100% Complete � Navigate to Chat Screen]
    |
Screen 2: Chat Screen (Full Width)
    |
  [Agent shows what it understood from screenshot + text]
  [User confirms or provides corrections]
    |
  [User: "Looks good, generate the dashboard!"]
    |
  [Chat transitions to left 30%, Dashboard appears on right 70%]
    |
Screen 3: Dashboard View (Split Screen)
    |
  [Left: Chat for refinements | Right: Live dashboard]
    |
  [Maximize button to display dashboard fullscreen]
```

## Screen Breakdown

### Screen 1: Upload Screen

**Purpose**: Collect user inputs to generate dashboard

#### Components

1. **Header Section**
   - Logo/branding: "DrawDash"
   - Tagline: "Transform sketches into dashboards instantly"
   - Navigation: (minimal, just home/about)

2. **Main Upload Area** (3 input sections, arranged vertically or in cards)

   **a) Dataset Upload** (Required) P
   - Drag-and-drop zone or file picker
   - Accepted formats: CSV, JSON, Parquet
   - File size limit indicator (e.g., "Max 10MB")
   - Preview: Show filename, size, number of rows/columns after upload
   - Remove/replace option

   **b) Screenshot Upload** (Required) P
   - Drag-and-drop zone or file picker
   - Accepted formats: PNG, JPG, JPEG
   - Thumbnail preview after upload
   - Remove/replace option

   **c) Clarification Text** (Optional)
   - Multi-line text box (textarea)
   - Placeholder: "Add any clarifications about your dashboard (e.g., 'Show last 30 days', 'Group by region', 'Use blue color scheme')"
   - Character limit: 1000 characters
   - Helper text: "Optional: Provide additional context to help us understand your requirements"

3. **Action Button / Progress Bar**
   - **Initial State**: Large, prominent "Upload" button
     - Disabled until both required fields (dataset + screenshot) are uploaded
     - Primary color, clear call-to-action

   - **Loading State**: Button transforms into inline progress bar
     - Shows percentage: 0% � 100%
     - Stage indicators below progress bar:
       - Stage 1: "Uploading data to DuckDB..." (0-50%)
       - Stage 2: "Understanding your requirements..." (50-100%)
     - Smooth animation transition from button to progress bar

   - **Complete State**:
     - Success checkmark with "Understanding complete!"
     - Auto-navigate to Chat Screen after 1 second

4. **Footer**
   - Help/FAQ link
   - Example templates: "See examples" link

#### Layout Suggestions
- Clean, centered layout
- Card-based design for each upload section
- Visual indicators for required vs optional fields
- Responsive: Stack vertically on mobile

---

### Screen 2: Chat Screen (Full Width)

**Purpose**: Agent presents its understanding and gets user confirmation before generating dashboard

#### Initial Layout (Full Width Chat)

```
+----------------------------------------------------------+
|                     Header                                |
+----------------------------------------------------------+
|                                                           |
|                   Chat Messages                           |
|                   (Centered, max-width)                   |
|                                                           |
+----------------------------------------------------------+
|                   Chat Input                              |
+----------------------------------------------------------+
```

#### Components

1. **Header**
   - Back button (return to upload screen)
   - Title: "Review Requirements"
   - Dataset name indicator

2. **Initial Agent Message** (Auto-displayed on page load)

   Example format:
   ```
   =K I've analyzed your screenshot and description. Here's what I understood:

   =� **Dashboard Title**: Sales Performance Q1 2024

   **Visualizations Requested**:
   1. =� Bar Chart
      - Title: "Revenue by Region"
      - X-axis: Region
      - Y-axis: Total Revenue
      - Aggregation: Sum

   2. =� Line Chart
      - Title: "Sales Trend Over Time"
      - X-axis: Date
      - Y-axis: Daily Sales
      - Time Range: Last 30 days

   3. >g Pie Chart
      - Title: "Market Share by Product Category"
      - Values: Percentage of total sales

   **Filters Detected**:
   - Date range: Last 30 days
   - Region: All regions

   **Additional Notes**:
   - Color scheme: Blue gradient
   - Show data labels on charts

   ---

   Does this match your requirements? You can:
    Reply "Looks good!" to generate the dashboard
    Request changes (e.g., "Change chart 2 to a bar chart")
   � Add more visualizations
   ```

3. **Chat History**
   - Scrollable message list
   - Agent messages (left-aligned, with avatar/icon)
   - User messages (right-aligned)
   - Markdown rendering support
   - Syntax highlighting for technical terms

4. **Chat Input** (Bottom, fixed)
   - Text input box
   - Placeholder: "Confirm or request changes..."
   - Send button
   - Character counter (optional)
   - Auto-focus on page load

5. **Quick Actions** (Above input, optional)
   - Suggested responses as chips:
     - "Looks good, generate!"
     - "Add a filter"
     - "Change chart type"
     - "Modify time range"

#### Interaction Flow

1. **User Reviews** the agent's understanding
2. **User Responds** with either:
   - Confirmation: "Looks good!", "Generate the dashboard", "Perfect!"
   - Modifications: "Change the bar chart to a line chart", "Add a pie chart for categories"
3. **Agent Confirms** changes and updates the specification
4. **Once User Confirms** � Agent starts generating dashboard
   - Show "Generating your dashboard..." message with spinner
   - Transition to Split View

---

### Screen 3: Dashboard View (Split Screen)

**Purpose**: Display generated dashboard and allow iterative refinements

#### Layout Transition

**Before Dashboard Generation** (Screen 2):
- Chat takes full width (centered, max-width 800px)

**After Dashboard Generation** (Screen 3):
- Smooth animated transition
- Chat slides to left (30% width)
- Dashboard slides in from right (70% width)

#### Split Layout
```
+------------------+----------------------------------+
|                  |                                  |
|   Chat Panel     |    Dashboard Panel               |
|   (Left 30%)     |    (Right 70%)                   |
|                  |                                  |
+------------------+----------------------------------+
```

#### Left Panel: Chat Interface (30% width)

1. **Chat Header**
   - Title: "Chat"
   - Collapse button (hide chat, expand dashboard to 100%)

2. **Chat History**
   - Continues from Screen 2
   - New system message: " Dashboard generated! You can now request refinements."
   - All previous messages preserved

3. **Suggested Refinements** (Contextual chips)
   - "Change colors"
   - "Add filters"
   - "Export dashboard"
   - "Modify chart type"

4. **Chat Input**
   - Text input at bottom
   - Placeholder: "Request changes or refinements..."
   - Send button

#### Right Panel: Dashboard Preview (70% width)

1. **Dashboard Header**
   - Dashboard title (extracted from screenshot, editable inline)
   - Actions:
     - **Maximize button** =2 (Fullscreen mode)
     - **Export button** =� (Export as HTML/PNG/PDF)
     - **Refresh button** = (Re-run queries)

2. **Dashboard Canvas**
   - Rendered interactive visualizations
   - Layout matches original screenshot as closely as possible
   - Interactive features:
     - Hover tooltips on data points
     - Clickable legends
     - Zoomable/pannable charts (where applicable)
     - Cross-filtering (click one chart to filter others)

3. **Loading Indicator** (When updating)
   - Semi-transparent overlay with spinner
   - Message: "Updating dashboard..."
   - Appears when user requests changes via chat

#### Fullscreen Mode (Maximize)

When user clicks maximize button:
- Chat panel hides (slides out left)
- Dashboard expands to 100% width
- Header shows "Exit Fullscreen" button
- Floating chat button in bottom-right corner
  - Click to bring back chat panel temporarily (modal or slide-in)

#### Responsive Behavior
- **Desktop** (>1200px): Split view as described
- **Tablet** (768-1200px):
  - Chat: 40% width
  - Dashboard: 60% width
- **Mobile** (<768px):
  - Tab navigation between Chat and Dashboard
  - Default to Dashboard tab
  - Badge indicator on Chat tab for new messages

---

## Technical Requirements

### Frontend Framework Options

**Recommended: Streamlit** (for hackathon MVP)
- Pros:
  - Fastest development time
  - Built-in chat interface (`st.chat_message`, `st.chat_input`)
  - Easy file uploads
  - Native Python visualization support
  - Can embed custom HTML/CSS for layouts
- Cons:
  - Less control over animations
  - Requires some custom CSS for split view

**Alternative: Gradio**
- Pros: AI-friendly, simple blocks-based layout
- Cons: Limited chat interface customization

**Alternative: React + FastAPI**
- Pros: Full control, professional UX
- Cons: Longer development time (not ideal for hackathon)

### Core Features

1. **File Upload**
   - Client-side validation (file type, size)
   - Progress indicator for large files
   - Drag-and-drop support
   - Preview after upload

2. **Progress Bar Animation**
   - CSS transition from button to progress bar
   - Smooth percentage updates (animate from 0% to target)
   - Stage transitions with fade effect

3. **Real-time Updates**
   - WebSocket or polling for agent status updates
   - Server-sent events (SSE) for progress percentage
   - Chat message streaming (typing effect)

4. **Dashboard Rendering**
   - Embedded visualization library (Plotly recommended)
   - Responsive container sizing
   - Export functionality (HTML, PNG, PDF)
   - Interactive features (zoom, pan, filter)

5. **Chat Interface**
   - Markdown rendering for agent responses
   - Syntax highlighting for code/SQL snippets
   - Auto-scroll to latest message
   - Message history persistence
   - Typing indicator when agent is processing

### State Management

**Screen 1 State**:
```python
{
  "datasetFile": File | null,
  "screenshotFile": File | null,
  "clarificationText": str,
  "uploadStatus": "idle" | "uploading" | "processing" | "complete",
  "progress": 0-100
}
```

**Screen 2 State**:
```python
{
  "chatHistory": List[Message],
  "agentUnderstanding": Dict,  # Parsed requirements
  "isTyping": bool,
  "isConfirmed": bool
}
```

**Screen 3 State**:
```python
{
  "dashboardData": Dict,  # Chart configs, data
  "chatHistory": List[Message],
  "isUpdating": bool,
  "isFullscreen": bool,
  "isChatVisible": bool
}
```

---

## Design Considerations

### Visual Style
- **Modern, clean interface** (inspired by Notion, Linear)
- **Color scheme**:
  - Primary: Professional blue (#2563eb)
  - Success: Green (#10b981)
  - Background: Light gray/white (#f9fafb)
- **Typography**: Clear, readable fonts (Inter, SF Pro)
- **Spacing**: Generous whitespace for clarity

### Animations
- Button � Progress bar: 300ms ease-out
- Screen transitions: 400ms slide-in
- Chat � Split view: 500ms with easing
- Dashboard updates: Fade overlay 200ms

### Accessibility
- ARIA labels for all interactive elements
- Keyboard navigation support
- Focus indicators
- High contrast mode support
- Screen reader friendly messages

### Error Handling

**Upload Errors**:
- "File format not supported. Please upload CSV, JSON, or Parquet."
- "File size exceeds 10MB limit. Please upload a smaller file."
- "Failed to upload file. Please check your connection and try again."

**Processing Errors**:
- "Failed to understand screenshot. Please upload a clearer image."
- "Could not load dataset into DuckDB. Please check the file format."
- Toast notification: "Something went wrong. Please try again."

**Chat Errors**:
- "Message failed to send. Retrying..."
- "Agent is taking longer than expected. Please wait..."

---

## MVP Feature Priority

### Must Have (Phase 1) - Hackathon MVP
-  Upload screen with 3 inputs (dataset, screenshot, text)
-  Button � Progress bar transformation
-  Full-width chat screen showing agent understanding
-  Confirmation flow (user approves or corrects)
-  Split view with chat (left) and dashboard (right)
-  Basic dashboard rendering with Plotly
-  Chat refinements (modify dashboard)

### Nice to Have (Phase 2)
- Maximize/fullscreen mode for dashboard
- Export dashboard as HTML/PNG
- Example templates gallery
- Quick action chips in chat
- Typing indicators

### Future Enhancements (Phase 3)
- Save/load previous projects
- Collaborative editing
- Real-time data refresh
- Mobile app
- Dashboard templates library
