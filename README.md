# 🧠 Knowledge Graph-Based Personalized Skill & Project Recommendation System

A Python-based student recommendation system that uses **Knowledge Graph relationships and reasoning** to recommend relevant skills and projects based on a student's existing skills, academic level, and areas of interest. The application also includes a **Live Internships** section that retrieves technical internship listings from an external API.

## 📌 Project Overview

Students often struggle to decide which skills to learn next, which projects match their current abilities, and where to find relevant internship opportunities.

This project addresses these challenges by representing students, skills, domains, and projects as a Knowledge Graph. Relationships between these entities help the system evaluate skill relevance, check prerequisites, match project requirements, and generate explainable recommendations.

The application is built using Python and Streamlit, with NetworkX for graph operations. It does not require Neo4j.

## ✨ Features

### 👤 1. Student Profile

- Select a student profile from the application sidebar.
- View the student's academic level, interest domain, and current skills.
- Use profile information as input to the recommendation engine.

### 💡 2. Personalized Skill Recommendations

- Recommend skills relevant to the student's existing skills and interests.
- Use Knowledge Graph relationships to identify related skills.
- Consider prerequisite requirements before presenting recommendations.
- Display recommendation scores and explanations.
- Identify missing prerequisites so students can understand what to learn first.

### 🚀 3. Personalized Project Recommendations

- Recommend projects based on the student's profile and skills.
- Match project requirements against skills the student already possesses.
- Display project domains and recommendation scores.
- Identify missing skills needed to complete a recommended project.
- Explain why each project is a relevant match.

### 🕸️ 4. Interactive Knowledge Graph Visualization

- Explore relationships between students, skills, domains, and projects.
- Visualize related skills, prerequisites, and project requirements.
- Generate an interactive graph for the selected student.
- Use graph relationships to make recommendation results easier to understand.

### 🌐 5. Live Internship Listings

The application integrates with the **OpenIntern public API** to retrieve internship listings.

- Fetch internship postings from an external service.
- Filter listings using technical keywords such as Java, Python, software development, data science, machine learning, AI, web development, cybersecurity, and cloud computing.
- Display available internship details, including title, company, location, posting date when provided, and application link.
- Remove duplicate listings while preserving their order.
- Handle API errors and timeouts by returning an appropriate failure response.

**Important:** Internship availability depends on the external API. Listings, locations, posting dates, and application links may change, and the API may occasionally be unavailable.

## 🧩 Knowledge Graph Design

The Knowledge Graph is implemented using Python and NetworkX.

### Main entities

| Entity | Purpose |
|---|---|
| Student | Represents a student profile |
| Skill | Represents a technical or professional skill |
| Project | Represents a project that can be recommended |
| Domain | Represents an area of interest or specialization |

### Main relationships

| Relationship | Purpose |
|---|---|
| `HAS_SKILL` | Connects a student to a skill they possess |
| `INTERESTED_IN` | Represents a student's interest domain |
| `RELATED_TO` | Connects related skills |
| `PREREQUISITE_OF` | Represents prerequisite dependencies between skills |
| `BELONGS_TO` | Associates a skill with a domain |
| `REQUIRES` | Connects a project to its required skills |
| `PART_OF` | Represents part-of relationships |
| `SUBDOMAIN_OF` | Represents domain hierarchy |

The graph structure allows the recommendation engine to use relationships between entities instead of relying only on isolated keyword matches.

## ⚙️ Recommendation Workflow

1. **Student selection:** Load the selected student's profile and existing skills.
2. **Graph analysis:** Use the Knowledge Graph to identify relevant skills, domains, prerequisites, and project requirements.
3. **Candidate generation:** Identify candidate skills and projects for the selected student.
4. **Prerequisite checking:** Determine whether required prerequisite skills are satisfied.
5. **Scoring and ranking:** Calculate recommendation scores and rank suitable candidates.
6. **Explanation generation:** Show why a skill or project is recommended and identify missing skills where applicable.
7. **Visualization:** Display the relevant Knowledge Graph to help users explore the relationships.

### Workflow overview

```text
Student Profile
      |
      v
Knowledge Graph
      |
      v
Skill and Prerequisite Analysis
      |
      v
Skill Recommendations
      |
      v
Project Requirement Matching
      |
      v
Project Recommendations
      |
      v
Scores and Explanations
      |
      v
Interactive Graph Visualization
```

The Live Internships feature uses a separate API integration to retrieve external internship listings.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and recommendation logic |
| Streamlit | Interactive web interface |
| Pandas | Loading and processing structured CSV data |
| NetworkX | Knowledge Graph representation and graph operations |
| PyVis | Interactive graph visualization |
| SQLite | Local database functionality used by the application |
| OpenIntern API | External source for live internship listings |
| Git and GitHub | Version control and project hosting |

## 📂 Project Structure

```text
kg_skill_project_prototype/
│
├── app.py
├── knowledge_graph.html
├── .gitignore
├── README.md
│
├── data/
│   ├── sample_students.csv
│   ├── skills.csv
│   ├── domains.csv
│   ├── skill_domains.csv
│   ├── skill_prerequisites.csv
│   ├── skill_related.csv
│   ├── projects.csv
│   ├── project_skills.csv
│   ├── courses.csv
│   ├── course_skills.csv
│   ├── internships.csv
│   ├── internship_skills.csv
│   └── student_knowledge_graph.html
│
├── database/
│   ├── database.py
│   └── check_database.py
│
├── src/
│   ├── knowledge_graph.py
│   ├── visualization.py
│   ├── admin/
│   │   └── data_ingestion.py
│   ├── auth/
│   │   ├── authentication.py
│   │   └── create_admin.py
│   ├── integrations/
│   │   └── internship_api.py
│   └── recommender/
│       ├── recommendation_engine.py
│       ├── prerequisites.py
│       ├── skill_candidates.py
│       ├── project_candidates.py
│       ├── scoring.py
│       ├── project_scoring.py
│       ├── explanations.py
│       ├── course_recommendation.py
│       ├── internship_recommendation.py
│       ├── learning_roadmap.py
│       ├── natural_language_query.py
│       └── skill_gap.py
│
├── lib/
├── tests/
└── venv/
```

*Note: The structure above highlights the main files. Some files and folders may vary as development continues. The local virtual environment and database files should not be committed to GitHub.*

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or later is recommended.
- Git
- Visual Studio Code or another Python editor
- Internet access for retrieving live internship listings

### 1. Clone the repository

```bash
git clone https://github.com/Deepthika-209/knowledge-graph-skill-project.git
cd knowledge-graph-skill-project
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

Install the packages required by the application:

```powershell
python -m pip install streamlit pandas networkx pyvis
```

If the application reports a missing package when starting, install that package in the activated virtual environment. A dependency file such as `requirements.txt` can be added to make installation reproducible.

### 5. Run the application

From the project root directory, run:

```powershell
streamlit run app.py
```

Streamlit will display a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

## 📊 Data Sources

The project uses structured CSV files to represent the Knowledge Graph and recommendation inputs.

- **Student profiles:** sample student identifiers, skills, academic levels, and interests.
- **Skills and domains:** skill definitions and their domain associations.
- **Prerequisites:** dependencies between skills.
- **Related skills:** relationships used to identify relevant skills.
- **Projects and project skills:** project definitions and their required skills.
- **Courses and course skills:** structured information for course-related recommendations.
- **Internship data:** local internship-related data files, alongside the separate OpenIntern API integration.

The sample CSV files support demonstration and testing. Replace or extend the sample data with appropriate data before using the system in a real institutional environment.

## 🔐 Security and Privacy

- Keep passwords, API credentials, and other secrets out of source control.
- The `.gitignore` file excludes common local database files, Python caches, and virtual environments.
- Use appropriate access controls before deploying the application for real students.
- Review the authentication and admin functionality before exposing the application publicly.
- Avoid committing real student personal information to a public repository.

## 🎯 Project Objectives

The main objectives of this project are to:

1. Apply Knowledge Graph concepts to a practical student recommendation problem.
2. Recommend relevant skills using graph relationships and prerequisite reasoning.
3. Match student skills against project requirements.
4. Provide understandable explanations for recommendation results.
5. Visualize relationships between students, skills, domains, and projects.
6. Extend career preparation support through live technical internship listings.
7. Demonstrate a Python-based graph recommendation system without requiring Neo4j.

## 🔮 Future Enhancements

- Add a verified `requirements.txt` for easier installation.
- Improve the ranking algorithm using additional student feedback and evaluation.
- Add filters for internship location, role, and recency where supported by the data source.
- Improve API caching and provide a clearer fallback when the internship service is unavailable.
- Add more student profiles, skills, domains, projects, and courses.
- Expand automated testing for recommendation quality and prerequisite validation.
- Add deployment instructions for a hosted Streamlit application.

## 👩‍💻 Author

**Deepthika Miriyala**

Project: Knowledge Graph-Based Personalized Skill & Project Recommendation System

[GitHub Repository](https://github.com/Deepthika-209/knowledge-graph-skill-project)
