# defi-credit-scoring
DeFi Wallet Credit Scoring System for Aave V2 By S V K

# DeFi Wallet Credit Scoring System

A comprehensive machine learning-based credit scoring system for DeFi wallets using Aave V2 protocol transaction data.

## Overview

This system analyzes transaction patterns from Aave V2 protocol to assign credit scores (0-1000) to individual wallets. Higher scores indicate reliable, responsible usage patterns, while lower scores suggest risky or exploitative behavior.

## Architecture

### Core Components

1. **Data Processing Engine**: Loads and parses JSON transaction data
2. **Feature Engineering Module**: Extracts behavioral patterns and risk indicators
3. **Credit Scoring Algorithm**: Multi-dimensional scoring with weighted components
4. **Analysis & Visualization**: Score distribution analysis and behavioral insights

### Scoring Methodology

The credit scoring system evaluates wallets across six key dimensions:

#### 1. Repayment Behavior (Weight: 25%)
- **Repay-to-Borrow Ratio**: Measures loan repayment discipline
- **Calculation**: `repay_count / max(1, borrow_count)`
- **Interpretation**: Higher ratios indicate responsible borrowing

#### 2. Transaction Consistency (Weight: 20%)
- **Temporal Regularity**: Consistency in transaction timing
- **Calculation**: `1 / (1 + std_time_between_txns / avg_time_between_txns)`
- **Interpretation**: Regular patterns suggest genuine user behavior

#### 3. Protocol Engagement (Weight: 15%)
- **Depth of Usage**: Diversity and duration of protocol interaction
- **Components**: Unique functions used, transaction count, activity span
- **Interpretation**: Deep engagement indicates commitment to the ecosystem

#### 4. Risk Management (Weight: 15%)
- **Deposit-to-Borrow Ratio**: Collateralization patterns
- **Calculation**: `deposit_count / max(1, borrow_count)`
- **Interpretation**: Higher ratios show conservative risk management

#### 5. Liquidity Provision (Weight: 10%)
- **Deposit Activity**: Contribution to protocol liquidity
- **Measurement**: Normalized deposit transaction count
- **Interpretation**: Liquidity providers support protocol stability

#### 6. Protocol Usage Diversity (Weight: 10%)
- **Function Variety**: Range of protocol features used
- **Measurement**: Count of unique function calls
- **Interpretation**: Diverse usage suggests sophisticated understanding

#### 7. Liquidation Penalty (Weight: 5%)
- **No Liquidations Bonus**: Reward for avoiding liquidations
- **Binary Score**: 1.0 if no liquidations, 0.0 otherwise
- **Interpretation**: Liquidation history indicates poor risk management

### Feature Engineering

The system extracts 25+ features from raw transaction data:

#### Transaction Metrics
- Total transactions, unique functions, value patterns
- Average, median, and standard deviation of transaction values
- Gas usage efficiency indicators

#### Temporal Features
- Activity span, transaction frequency, timing consistency
- Time intervals between transactions
- Regularity patterns

#### Behavioral Indicators
- Function-specific counts (deposit, borrow, repay, redeem, liquidation)
- Behavioral ratios and risk indicators
- Protocol engagement depth

#### Risk Factors
- Liquidation events, high-value usage patterns
- Borrowing frequency, repayment discipline
- Volatility in transaction patterns

### Machine Learning Components

#### Clustering Analysis
- **Algorithm**: K-Means clustering (5 clusters)
- **Purpose**: Identify distinct behavioral patterns
- **Impact**: Cluster-based score adjustments (0.8x to 1.2x multipliers)

#### Scaling and Normalization
- **Method**: RobustScaler for feature standardization
- **Purpose**: Handle outliers and ensure equal feature weighting
- **Benefits**: Improved model stability and interpretability

## Usage

### Installation

```bash
# Install required dependencies
pip install pandas numpy scikit-learn matplotlib seaborn

# Clone repository
git clone <repository-url>
cd defi-credit-scoring
```

### Running the Analysis

```bash
# Basic usage
python credit_scorer.py path/to/transaction_data.json

# Example with sample data
python credit_scorer.py user_transactions.json
```

### Output Files

The system generates three output files:

1. **wallet_credit_scores.csv**: Wallet addresses and their credit scores
2. **score_analysis.json**: Detailed analysis by score ranges
3. **credit_score_analysis.png**: Visualization of score distribution

## Processing Flow

```
Raw JSON Data → Feature Engineering → Scoring Algorithm → Analysis & Visualization
      ↓                    ↓                  ↓                     ↓
- Transaction data    - 25+ features     - Weighted scoring    - Distribution plots
- Wallet addresses    - Behavioral metrics- Cluster adjustments- Range analysis
- Function calls      - Risk indicators  - 0-1000 scale       - Behavioral insights
```

## Score Interpretation

### Score Ranges

- **900-1000**: Excellent credit - Highly reliable, consistent users
- **800-899**: Very Good - Strong repayment history, regular usage
- **700-799**: Good - Responsible behavior with minor inconsistencies
- **600-699**: Fair - Moderate risk with some concerning patterns
- **500-599**: Poor - High risk, irregular behavior
- **0-499**: Very Poor - Extremely risky, potential bot/exploit activity

### Key Behavioral Indicators

#### High-Score Wallets (800+)
- Consistent repayment patterns (repay/borrow ratio > 1.0)
- Regular transaction timing
- Diverse protocol usage
- No liquidation history
- Strong collateralization patterns

#### Low-Score Wallets (0-300)
- Poor repayment discipline
- Irregular or bot-like transaction patterns
- High liquidation rates
- Limited protocol engagement
- Risky borrowing behavior

## Model Validation

### Validation Approach
- **Cross-validation**: 5-fold validation on synthetic targets
- **Cluster Analysis**: Behavioral pattern identification
- **Domain Expertise**: Financial risk assessment principles
- **Outlier Detection**: Identification of anomalous patterns

### Performance Metrics
- Score distribution analysis
- Behavioral correlation validation
- Range-based characteristic analysis
- Feature importance assessment

## Transparency and Extensibility

### Design Principles
1. **Interpretability**: Clear scoring components and weights
2. **Transparency**: Open-source implementation with detailed documentation
3. **Extensibility**: Modular design for easy feature addition
4. **Validation**: Comprehensive analysis and visualization tools

### Future Enhancements
- Time-series analysis for trend identification
- Network analysis for wallet relationship mapping
- Real-time scoring updates
- Additional protocol integration
- Advanced ML models (neural networks, ensemble methods)

## Technical Requirements

- Python 3.7+
- pandas, numpy, scikit-learn
- matplotlib, seaborn for visualization
- JSON support for data loading

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create Pull Request

## License

MIT License - See LICENSE file for details
