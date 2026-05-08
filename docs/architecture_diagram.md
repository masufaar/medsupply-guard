# Architecture Diagram

```mermaid
flowchart TD
    subgraph Data Sources
        C1[Inventory CSV]
        C2[Demand History CSV]
        C3[Suppliers CSV]
        C4[Pending Orders CSV]
    end

    subgraph MedSupply Guard Engine
        DAE[Deterministic Analytics Engine\n(Python Pandas)]
        SG[Safety Guardrail\n(Regex / Pattern Matcher)]
    end
    
    subgraph Streamlit Application
        UI[Streamlit UI Dashboard]
        Context[Structured Analytics Context]
    end

    subgraph Language Model
        GC[GemmaClient Interface]
        MB[Mock Backend\n(For Testing/Offline Demo)]
        OB[Ollama Backend\n(gemma4:e2b)]
    end

    %% Data flow
    C1 --> DAE
    C2 --> DAE
    C3 --> DAE
    C4 --> DAE

    DAE --> Context
    Context --> UI
    
    UI --> SG
    
    %% Q&A and Requests Flow
    SG -- "Safe Request" --> GC
    SG -- "Clinical Advice Request" --> Refusal[Refusal Message]
    Refusal --> UI
    
    GC --> MB
    GC --> OB
    
    MB -. "Deterministic Responses" .-> UI
    OB -. "Grounded Generations" .-> UI
    
    classDef safe fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef warning fill:#fff3cd,stroke:#ffc107,stroke-width:2px;
    classDef blocked fill:#f8d7da,stroke:#dc3545,stroke-width:2px;
    
    class SG safe;
    class Refusal blocked;
    class DAE safe;
```
