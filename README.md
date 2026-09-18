\# Knowledge Graph-Based Personalized Skill \& Project Recommendation System



A Knowledge Graph-based recommendation system that recommends personalized skills and projects for students based on their current skills, proficiency levels, and interest domains.



\## Project Overview



The system represents students, skills, domains, and projects as nodes in a Knowledge Graph. Relationships such as prerequisites, related skills, project requirements, and student skills are used to generate personalized recommendations.



\## Main Features



\- Student profile-based recommendations

\- Skill recommendations using Knowledge Graph relationships

\- Prerequisite-based reasoning

\- Personalized project recommendations

\- Explainable recommendations

\- Interactive Knowledge Graph visualization

\- Recommendation scoring and ranking

\- Evaluation across multiple student profiles

\- Streamlit-based web interface



\## Knowledge Graph



The Knowledge Graph is implemented using Python and NetworkX.



\### Main Entities



\- Student

\- Skill

\- Project

\- Domain



\### Main Relationships



\- HAS\_SKILL

\- INTERESTED\_IN

\- RELATED\_TO

\- PREREQUISITE\_OF

\- BELONGS\_TO

\- REQUIRES

\- PART\_OF

\- SUBDOMAIN\_OF



\## Recommendation Process



Student Profile  

↓  

Knowledge Graph  

↓  

Skill and Prerequisite Analysis  

↓  

Skill Recommendation  

↓  

Project Requirement Matching  

↓  

Project Recommendation  

↓  

Explanation  

↓  

Visualization



\## Dataset



The project uses structured CSV files containing:



\- Domains

\- Skills

\- Skill-domain relationships

\- Skill prerequisites

\- Related skills

\- Projects

\- Project-skill requirements

\- Sample student profiles



\## Technology Stack



\- Python

\- Pandas

\- NetworkX

\- Streamlit

\- PyVis



The project is implemented completely using Python without Neo4j.



\## Project Structure



```text

kg\_skill\_project\_prototype/

├── data/

├── src/

│   └── recommender/

├── tests/

├── app.py

├── knowledge\_graph.html

├── README.md

└── .gitignore

Running the Project



Activate the virtual environment and run:



streamlit run app.py



The application provides a student selection interface, personalized skill and project recommendations, explanations, and Knowledge Graph visualization.



Evaluation



The current implementation was tested using 25 sample student profiles.



Student profiles tested: 25

Skill recommendation coverage: 96%

Project recommendation coverage: 100%

Known skills incorrectly recommended: No

Zero-score projects returned: No

Recommendation explanations generated: Yes

Project Purpose



The project demonstrates how Knowledge Graph concepts can be applied to a practical personalized recommendation problem using graph relationships, traversal, reasoning, scoring, and explainable recommendations.



Author



Deepthika Miriyala

