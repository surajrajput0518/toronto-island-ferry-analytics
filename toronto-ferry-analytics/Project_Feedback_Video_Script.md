# Project Presentation & Feedback Video Script: Toronto Island Ferry Analytics

**Intern Name:** Suraj Rajput  
**Internship Organization:** Unified Mentor  
**Project Title:** Real-Time Ferry Ticket Sales & Redemption Analytics for Toronto Island Park  
**Target Duration:** 3 to 5 Minutes  
**Recommended Recording Tools:** Loom (free, browser extension), OBS Studio, or Google Meet (start a solo meeting and hit "Record Screen").

---

## 🎬 Quick Recording Checklist
1. Have your **Streamlit Web Application** open and running in full screen on your browser (`localhost:8501` or your deployed Streamlit Cloud URL).
2. Keep your webcam enabled in the corner if possible (adds a personal touch for evaluators).
3. Speak clearly, confidently, and maintain an enthusiastic tone.

---

## 📜 Full Word-for-Word Video Script

### ⏱️ Segment 1: Introduction & Problem Context (0:00 – 0:45)
**[Visual: Start with your webcam or showing the Title Header of your Streamlit Dashboard]**

> *"Hello everyone! My name is Suraj Rajput, and I am excited to present my internship capstone project completed with Unified Mentor: **Real-Time Ferry Ticket Sales & Redemption Analytics for Toronto Island Park**.*
>
> *Toronto Island Park is one of Canada's most beloved urban recreational treasures, hosting over 1.4 million visitors every year. Ferries operate year-round from the Jack Layton Ferry Terminal across three primary destinations: Centre Island, Hanlan’s Point, and Ward’s Island.*
>
> *Despite having granular 15-minute transactional ticketing data, terminal operations historically relied on static timetables. During peak summer weekends and sudden good-weather surges, passenger arrival rates would drastically outpace vessel capacity—causing terminal congestion, long passenger queues, and operational headaches.*
>
> *Our objective was to build an intelligent, centralized analytics system to identify peak passenger bottlenecks, track real-time net passenger movement, forecast upcoming demand using Machine Learning, and provide data-driven ferry dispatch recommendations."*

---

### ⏱️ Segment 2: Dataset Architecture & High-Level KPIs (0:45 – 1:30)
**[Visual: Navigate to Tab 1: 'Executive Overview & Live KPIs' — point cursor at the metric cards and the interactive timeline]**

> *"Let me walk you through the live Streamlit dashboard. First, let's look at the sheer scale of the dataset we analyzed.*
>
> *We processed over **261,000 continuous 15-minute intervals** spanning more than **10.5 years**—from May 2015 all the way to December 2025. Across this decade, the terminal recorded **12.97 million ticket sales** and **12.78 million redemptions**.*
>
> *On this main Overview tab, stakeholders immediately see live operational KPIs:*
> - *Total volume breakdown and current Net Passenger Movement.*
> - *The Off-Season Utilization Index, showing that winter operations drop to just **5.1%** of summer peak volume.*
> - *And an interactive time-series timeline where operators can drill down into any year, month, or day to view sales versus redemptions side-by-side."*

---

### ⏱️ Segment 3: Deep Dive Analytics & Peak Congestion Heatmaps (1:30 – 2:30)
**[Visual: Switch to Tab 2: 'Temporal Flow & Peak Heatmap' — hover over the colored heatmap grid]**

> *"Now, looking at the **Peak Flow & Temporal Analysis**, we uncovered fascinating asymmetric dynamics:*
>
> *First, look at this Hour-of-Day versus Day-of-Week heatmap matrix. Notice the deep red cluster right here: Saturday and Sunday between **11:00 AM and 2:00 PM** experience extreme outbound surges, peaking at over **3,400 passengers per hour**.*
>
> *Second, we analyzed the return wave. Outbound traffic peaks at noon, but return traffic concentrates sharply between **5:30 PM and 8:30 PM**. Without predictive coordination, this creates massive return queues at Centre Island dock.*
>
> *Looking at our multi-year analysis in Tab 3, we also tracked the historical resilience of the system—from steady pre-pandemic growth, through the severe 68% dip during the 2020 lockdowns, to a robust post-pandemic recovery reaching 1.46 million passengers in 2025."*

---

### ⏱️ Segment 4: AI Demand Forecasting & Operations Fleet Simulator (2:30 – 3:45)
**[Visual: Switch to Tab 4: 'Fleet Scheduling Simulator' and move the sliders; then show Tab 5: 'AI Demand Forecasting']**

> *"What makes this platform actionable is our two advanced decision-support tools:*
>
> *Under the **Fleet Scheduling Simulator**, terminal managers can adjust the active vessels—such as the 1,000-passenger Trillium or 915-passenger Sam McBride—and set round-trip cycle times. The system instantly calculates the required departures per hour and sounds a backlog alert if incoming passenger volume exceeds active vessel throughput.*
>
> *Furthermore, in the **AI Forecasting Engine**, we developed an autoregressive machine learning model utilizing multi-scale lag features and cyclical trigonometric encodings. Achieving an **R² score of 0.914** and a Mean Absolute Error of under 19 passengers, the model forecasts expected passenger volume up to 48 hours in advance, enabling dispatchers to schedule crews proactively rather than reactively."*

---

### ⏱️ Segment 5: Learnings, Experience & Conclusion (3:45 – 4:30)
**[Visual: Switch back to full webcam or the Summary/About tab]**

> *"To conclude, my internship experience with Unified Mentor has been transformative. Working with real-world municipal Big Data—cleaning over a quarter-million timestamps, architecting time-series features, formulating queuing mechanics, and packaging everything into an end-to-end deployed web application—has significantly leveled up my skills in Data Science and Engineering.*
>
> *All source code, documentation, and the full IEEE-format research paper are available in my GitHub repository and linked in my submission.*
>
> *Thank you to my mentors at Unified Mentor and the Toronto Parks & Recreation team for this incredible learning opportunity. Thank you for watching!"*

---

## 📌 Submission Tips
1. Once recorded, upload the video to:
   - **YouTube** (set visibility to **Unlisted** so anyone with the link can view it), OR
   - **Google Drive** (make sure file sharing is set to **"Anyone with the link can view"**), OR
   - **Loom** (copy the direct share URL `https://www.loom.com/share/...`).
2. Verify that the URL begins with `https://`.
3. Paste the URL into the **"Project Feedback video link"** field on the submission form.
