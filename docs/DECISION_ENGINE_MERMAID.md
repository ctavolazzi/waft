# Decision Engine - Complete Mermaid Diagrams

**Purpose**: Visual representation of the entire decision engine architecture, flow, and data structures.

---

## System Architecture Overview

```mermaid
graph TB
    subgraph "User Interface Layer"
        CLI[waft decide<br/>CLI Command]
        API[Future: API Endpoint]
        UI[Future: Web UI]
    end

    subgraph "Interface Layer: DecisionCLI"
        DecisionCLI[DecisionCLI Class<br/>src/waft/core/decision_cli.py]
        RunMatrix[run_decision_matrix<br/>Main Entry Point]
        ValidateInput[Input Validation<br/>- Weights sum to 1.0<br/>- All scores present]
        BuildData[Build Data Structures<br/>- Alternative objects<br/>- Criterion objects<br/>- Score objects]
        DisplayResults[_display_results<br/>Rich formatted output]
    end

    subgraph "Mathematical Layer: DecisionMatrixCalculator"
        Calculator[DecisionMatrixCalculator<br/>src/waft/core/decision_matrix.py]
        ValidateMatrix[Matrix Validation<br/>- Weights sum to 1.0<br/>- All alternatives scored]
        WSM[calculate_wsm<br/>Weighted Sum Model]
        WPM[calculate_wpm<br/>Weighted Product Model]
        AHP[calculate_ahp_weights<br/>Analytic Hierarchy Process]
        BWM[calculate_bwm_weights<br/>Best Worst Method]
        Rank[rank_alternatives<br/>Sort by score]
        Details[get_detailed_scores<br/>Per-alternative breakdown]
        Sensitivity[sensitivity_analysis<br/>Weight variations]
    end

    subgraph "Data Structures"
        Alternative[Alternative<br/>dataclass]
        Criterion[Criterion<br/>dataclass]
        Score[Score<br/>dataclass]
        DecisionMatrix[DecisionMatrix<br/>dataclass]
    end

    CLI --> DecisionCLI
    API -.-> DecisionCLI
    UI -.-> DecisionCLI

    DecisionCLI --> RunMatrix
    RunMatrix --> ValidateInput
    ValidateInput -->|Valid| BuildData
    ValidateInput -->|Invalid| Error1[ValueError]

    BuildData --> Alternative
    BuildData --> Criterion
    BuildData --> Score

    Alternative --> DecisionMatrix
    Criterion --> DecisionMatrix
    Score --> DecisionMatrix

    DecisionMatrix --> Calculator
    Calculator --> ValidateMatrix
    ValidateMatrix -->|Valid| WSM
    ValidateMatrix -->|Valid| WPM
    ValidateMatrix -->|Valid| AHP
    ValidateMatrix -->|Valid| BWM
    ValidateMatrix -->|Invalid| Error2[ValueError]

    WSM --> Rank
    WPM --> Rank
    AHP --> Rank
    BWM --> Rank

    Rank --> Details
    Details --> Sensitivity
    Sensitivity --> DisplayResults
    DisplayResults --> CLI

    style DecisionCLI fill:#e1f5ff
    style Calculator fill:#fff4e1
    style ValidateInput fill:#ffe1e1
    style ValidateMatrix fill:#ffe1e1
    style WSM fill:#e1ffe1
    style WPM fill:#e1ffe1
    style AHP fill:#e1ffe1
    style BWM fill:#e1ffe1
    style DecisionMatrix fill:#f0e1ff
```

---

## Complete Data Flow

```mermaid
flowchart TD
    Start([User calls<br/>run_decision_matrix]) --> Input[Input Parameters<br/>problem, alternatives,<br/>criteria, scores]

    Input --> V1{Validate<br/>Weights<br/>Sum to 1.0?}
    V1 -->|No| E1[Raise ValueError<br/>Weights must sum to 1.0]
    V1 -->|Yes| V2{Validate<br/>All Alternatives<br/>Have Scores?}

    V2 -->|No| E2[Raise ValueError<br/>Missing alternative]
    V2 -->|Yes| V3{Validate<br/>All Criteria<br/>Present?}

    V3 -->|No| E3[Raise ValueError<br/>Missing criterion]
    V3 -->|Yes| Build[Build Data Structures]

    Build --> Alt[Create Alternative<br/>objects]
    Build --> Crit[Create Criterion<br/>objects]
    Build --> Sc[Create Score<br/>objects]

    Alt --> Matrix[Create DecisionMatrix<br/>dataclass]
    Crit --> Matrix
    Sc --> Matrix

    Matrix --> Calc[DecisionMatrixCalculator<br/>matrix]
    Calc --> V4{Validate Matrix<br/>Completeness}

    V4 -->|No| E4[Raise ValueError<br/>Missing scores]
    V4 -->|Yes| Method{Select<br/>Methodology}

    Method -->|WSM| WSM[calculate_wsm<br/>Σ weight × score]
    Method -->|WPM| WPM[calculate_wpm<br/>Π score^weight]
    Method -->|AHP| AHP[calculate_ahp_weights<br/>Pairwise comparisons]
    Method -->|BWM| BWM[calculate_bwm_weights<br/>Best/worst method]

    WSM --> Results[Results Dict<br/>alternative → score]
    WPM --> Results
    AHP --> Results
    BWM --> Results

    Results --> Rank[rank_alternatives<br/>Sort by score]
    Rank --> Rankings[Rankings List<br/>name, score, rank]

    Rankings --> Display[Display Results<br/>Rich tables]
    Display --> Sens{Sensitivity<br/>Analysis?}

    Sens -->|Yes| SensCalc[Calculate weight<br/>variations]
    Sens -->|No| Return
    SensCalc --> Return

    Return([Return Results<br/>Dict])

    style V1 fill:#ffe1e1
    style V2 fill:#ffe1e1
    style V3 fill:#ffe1e1
    style V4 fill:#ffe1e1
    style WSM fill:#e1ffe1
    style WPM fill:#e1ffe1
    style AHP fill:#e1ffe1
    style BWM fill:#e1ffe1
    style Matrix fill:#f0e1ff
```

---

## WSM Calculation Detail

```mermaid
flowchart TD
    Start([calculate_wsm called]) --> Init[Initialize results = {}]

    Init --> LoopAlt[For each alternative<br/>in matrix.alternatives]

    LoopAlt --> InitScore[total_score = 0.0]

    InitScore --> LoopCrit[For each criterion<br/>in matrix.criteria]

    LoopCrit --> FindScore[Find Score object<br/>matching alternative<br/>and criterion]

    FindScore --> Calc[Calculate weighted score<br/>weighted_score =<br/>criterion.weight ×<br/>score_obj.score]

    Calc --> Add[Add to total<br/>total_score +=<br/>weighted_score]

    Add --> MoreCrit{More<br/>criteria?}
    MoreCrit -->|Yes| LoopCrit
    MoreCrit -->|No| Store[Store result<br/>results[alt.name] =<br/>total_score]

    Store --> MoreAlt{More<br/>alternatives?}
    MoreAlt -->|Yes| LoopAlt
    MoreAlt -->|No| Return([Return results<br/>Dict[alt_name: score]])

    style Calc fill:#e1ffe1
    style FindScore fill:#fff4e1
```

---

## Validation Layers

```mermaid
graph TB
    subgraph "Layer 1: Input Validation (DecisionCLI)"
        V1[Validate Weights Sum to 1.0<br/>±0.01 tolerance]
        V2[Validate All Alternatives Present]
        V3[Validate All Criteria Present]
        V4[Validate Score Structure]
    end

    subgraph "Layer 2: Matrix Validation (DecisionMatrixCalculator)"
        V5[Validate Weights Sum to 1.0<br/>±0.01 tolerance]
        V6[Validate All Alternatives<br/>Scored on All Criteria]
        V7[Validate No Missing Scores]
    end

    subgraph "Layer 3: Calculation Validation"
        V8[Validate Methodology Supported]
        V9[Validate Scores Positive<br/>WPM only]
    end

    Input[User Input] --> V1
    V1 -->|Pass| V2
    V1 -->|Fail| Error1[ValueError:<br/>Weights don't sum to 1.0]

    V2 -->|Pass| V3
    V2 -->|Fail| Error2[ValueError:<br/>Missing alternative]

    V3 -->|Pass| V4
    V3 -->|Fail| Error3[ValueError:<br/>Missing criterion]

    V4 -->|Pass| Matrix[DecisionMatrix Created]
    V4 -->|Fail| Error4[ValueError:<br/>Invalid score structure]

    Matrix --> V5
    V5 -->|Pass| V6
    V5 -->|Fail| Error5[ValueError:<br/>Weights don't sum to 1.0]

    V6 -->|Pass| V7
    V6 -->|Fail| Error6[ValueError:<br/>Missing score]

    V7 -->|Pass| Calc[Calculation]
    V7 -->|Fail| Error7[ValueError:<br/>Incomplete matrix]

    Calc --> V8
    V8 -->|Pass| V9
    V8 -->|Fail| Error8[ValueError:<br/>Unsupported methodology]

    V9 -->|Pass| Results[Results Returned]
    V9 -->|Fail| Error9[ValueError:<br/>Invalid score value]

    style V1 fill:#ffe1e1
    style V2 fill:#ffe1e1
    style V3 fill:#ffe1e1
    style V4 fill:#ffe1e1
    style V5 fill:#ffe1e1
    style V6 fill:#ffe1e1
    style V7 fill:#ffe1e1
    style V8 fill:#ffe1e1
    style V9 fill:#ffe1e1
```

---

## Data Structure Relationships

```mermaid
erDiagram
    DecisionMatrix ||--o{ Alternative : contains
    DecisionMatrix ||--o{ Criterion : contains
    DecisionMatrix ||--o{ Score : contains
    Alternative ||--o{ Score : "has scores for"
    Criterion ||--o{ Score : "has scores from"

    DecisionMatrix {
        List[Alternative] alternatives
        List[Criterion] criteria
        List[Score] scores
        string methodology
    }

    Alternative {
        string name
        string description
    }

    Criterion {
        string name
        float weight
        string description
    }

    Score {
        string alternative_name
        string criterion_name
        float score
        string reasoning
    }

    DecisionMatrixCalculator {
        DecisionMatrix matrix
    }

    DecisionMatrixCalculator ||--|| DecisionMatrix : uses
```

---

## Method Selection Flow

```mermaid
flowchart TD
    Start([Calculator.calculate<br/>methodology parameter]) --> Check{Methodology<br/>Specified?}

    Check -->|Yes| Use[Use specified]
    Check -->|No| Default[Use matrix.methodology<br/>default: WSM]

    Use --> Route
    Default --> Route

    Route{Methodology<br/>Type?}

    Route -->|WSM| WSM[calculate_wsm<br/>Weighted Sum Model<br/>Σ weight × score]
    Route -->|WPM| WPM[calculate_wpm<br/>Weighted Product Model<br/>Π score^weight]
    Route -->|AHP| AHP[calculate_ahp_weights<br/>+ calculate_wsm<br/>Pairwise comparisons]
    Route -->|BWM| BWM[calculate_bwm_weights<br/>+ calculate_wsm<br/>Best/worst method]
    Route -->|Other| Error[ValueError<br/>Unsupported methodology]

    WSM --> Results[Results Dict]
    WPM --> Results
    AHP --> Results
    BWM --> Results

    Results --> Return([Return Results])

    style WSM fill:#e1ffe1
    style WPM fill:#e1ffe1
    style AHP fill:#e1ffe1
    style BWM fill:#e1ffe1
    style Error fill:#ffe1e1
```

---

## Sensitivity Analysis Flow

```mermaid
flowchart TD
    Start([Sensitivity Analysis<br/>Enabled]) --> Select[Select First Criterion]

    Select --> Test1[Test Weight -20%<br/>test_weight = weight × 0.8]
    Test1 --> Adjust1[Adjust Other Weights<br/>Proportionally]
    Adjust1 --> Recalc1[Recalculate Results<br/>New matrix, new calculator]
    Recalc1 --> Rank1[Rank Alternatives]
    Rank1 --> Result1[Get Top Alternative]

    Select --> Test2[Test Weight +20%<br/>test_weight = weight × 1.2]
    Test2 --> Adjust2[Adjust Other Weights<br/>Proportionally]
    Adjust2 --> Recalc2[Recalculate Results<br/>New matrix, new calculator]
    Recalc2 --> Rank2[Rank Alternatives]
    Rank2 --> Result2[Get Top Alternative]

    Result1 --> Compare[Compare Results<br/>Same top alternative?]
    Result2 --> Compare

    Compare -->|Same| Robust[Recommendation Robust<br/>Across weight variations]
    Compare -->|Different| Sensitive[Recommendation Sensitive<br/>To weight changes]

    Robust --> Display[Display Sensitivity<br/>Results]
    Sensitive --> Display

    style Test1 fill:#fff4e1
    style Test2 fill:#fff4e1
    style Recalc1 fill:#e1ffe1
    style Recalc2 fill:#e1ffe1
    style Robust fill:#e1ffe1
    style Sensitive fill:#ffe1e1
```

---

## Component Interaction Sequence

```mermaid
sequenceDiagram
    participant User
    participant CLI as DecisionCLI
    participant Validator as Input Validator
    participant Builder as Data Builder
    participant Matrix as DecisionMatrix
    participant Calc as DecisionMatrixCalculator
    participant Method as Calculation Method
    participant Ranker as Ranker
    participant Display as Display Formatter

    User->>CLI: run_decision_matrix(...)

    CLI->>Validator: Validate weights sum to 1.0
    Validator-->>CLI: ✓ Valid

    CLI->>Builder: Build Alternative objects
    Builder-->>CLI: List[Alternative]

    CLI->>Builder: Build Criterion objects
    Builder-->>CLI: List[Criterion]

    CLI->>Builder: Build Score objects
    Builder-->>CLI: List[Score]

    CLI->>Matrix: DecisionMatrix(alternatives, criteria, scores)
    Matrix-->>CLI: DecisionMatrix instance

    CLI->>Calc: DecisionMatrixCalculator(matrix)
    Calc->>Calc: _validate_matrix()
    Calc-->>CLI: ✓ Validated

    CLI->>Method: calculator.calculate_wsm()
    Method->>Method: For each alternative:<br/>For each criterion:<br/>weighted_score = weight × score<br/>total += weighted_score
    Method-->>CLI: Dict[alternative: score]

    CLI->>Ranker: calculator.rank_alternatives(results)
    Ranker->>Ranker: Sort by score descending<br/>Assign ranks
    Ranker-->>CLI: List[(name, score, rank)]

    CLI->>Display: _display_results(...)
    Display->>Display: Format tables, rankings
    Display-->>User: Rich formatted output

    CLI-->>User: Return results dict
```

---

## Error Handling Flow

```mermaid
flowchart TD
    Start([Operation Starts]) --> Try{Try Operation}

    Try -->|Success| Success([Success])
    Try -->|Error| Catch{Catch Error Type}

    Catch -->|ValueError| VError[ValueError<br/>Invalid Input/Matrix]
    Catch -->|KeyError| KError[KeyError<br/>Missing Key]
    Catch -->|TypeError| TError[TypeError<br/>Wrong Type]
    Catch -->|Other| OError[Unexpected Error]

    VError --> VMsg[Display Specific<br/>Error Message<br/>+ Actionable Fix]
    KError --> KMsg[Display Missing Key<br/>+ Context]
    TError --> TMsg[Display Type Mismatch<br/>+ Expected Type]
    OError --> OMsg[Display Error Details<br/>+ Stack Trace]

    VMsg --> User[User Sees Error]
    KMsg --> User
    TMsg --> User
    OMsg --> User

    User --> Fix{User Fixes<br/>Input?}
    Fix -->|Yes| Retry([Retry Operation])
    Fix -->|No| Abort([Abort])

    Retry --> Start

    style VError fill:#ffe1e1
    style KError fill:#ffe1e1
    style TError fill:#ffe1e1
    style OError fill:#ffe1e1
    style Success fill:#e1ffe1
```

---

**These diagrams show every aspect of the decision engine: architecture, flow, validation, calculations, and error handling.**
