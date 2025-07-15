#!/usr/bin/env python3
"""
DeFi Wallet Credit Scoring System for Aave V2 Protocol
=====================================================

This script analyzes transaction data from Aave V2 protocol and assigns credit scores
to wallets based on their historical behavior patterns.

Usage:
    python credit_scorer.py <path_to_json_file>

Requirements:
    - pandas
    - numpy
    - scikit-learn
    - matplotlib
    - seaborn
    - json
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class DeFiCreditScorer:
    """
    A comprehensive credit scoring system for DeFi wallets based on Aave V2 transaction data.
    
    The scoring system evaluates wallets across multiple dimensions:
    - Transaction consistency and frequency
    - Risk management behavior
    - Protocol engagement depth
    - Liquidity provision patterns
    - Default/liquidation history
    """
    
    def __init__(self):
        self.scaler = RobustScaler()
        self.model = None
        self.feature_importance = None
        self.wallet_scores = {}
        
    def load_data(self, json_file_path):
        """Load and parse JSON transaction data."""
        print("Loading transaction data...")
        
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Parse timestamps
        df['timestamp'] = pd.to_datetime(df['timeStamp'], unit='s')
        df['blockNumber'] = df['blockNumber'].astype(int)
        df['value'] = df['value'].astype(float)
        
        print(f"Loaded {len(df)} transactions from {df['from'].nunique()} unique wallets")
        return df
    
    def engineer_features(self, df):
        """
        Engineer comprehensive features for credit scoring.
        
        Features include:
        - Transaction frequency and consistency
        - Risk management metrics
        - Protocol engagement depth
        - Liquidity patterns
        - Behavioral consistency
        """
        print("Engineering features...")
        
        wallet_features = []
        
        for wallet in df['from'].unique():
            wallet_txns = df[df['from'] == wallet].copy()
            wallet_txns = wallet_txns.sort_values('timestamp')
            
            features = {'wallet': wallet}
            
            # Basic transaction metrics
            features['total_transactions'] = len(wallet_txns)
            features['unique_functions'] = wallet_txns['functionName'].nunique()
            features['total_value_transacted'] = wallet_txns['value'].sum()
            features['avg_transaction_value'] = wallet_txns['value'].mean()
            features['median_transaction_value'] = wallet_txns['value'].median()
            features['std_transaction_value'] = wallet_txns['value'].std()
            
            # Time-based features
            time_span = (wallet_txns['timestamp'].max() - wallet_txns['timestamp'].min()).days
            features['activity_span_days'] = max(1, time_span)
            features['avg_transactions_per_day'] = features['total_transactions'] / features['activity_span_days']
            
            # Calculate time intervals between transactions
            if len(wallet_txns) > 1:
                time_diffs = wallet_txns['timestamp'].diff().dt.total_seconds() / 3600  # hours
                features['avg_time_between_txns'] = time_diffs.mean()
                features['std_time_between_txns'] = time_diffs.std()
                features['consistency_score'] = 1 / (1 + features['std_time_between_txns'] / max(1, features['avg_time_between_txns']))
            else:
                features['avg_time_between_txns'] = 0
                features['std_time_between_txns'] = 0
                features['consistency_score'] = 0
            
            # Function-specific analysis
            function_counts = wallet_txns['functionName'].value_counts()
            
            # Core DeFi behavior patterns
            features['deposit_count'] = function_counts.get('deposit', 0)
            features['borrow_count'] = function_counts.get('borrow', 0)
            features['repay_count'] = function_counts.get('repay', 0)
            features['redeem_count'] = function_counts.get('redeemUnderlying', 0)
            features['liquidation_count'] = function_counts.get('liquidationCall', 0)
            
            # Calculate behavioral ratios
            features['repay_to_borrow_ratio'] = features['repay_count'] / max(1, features['borrow_count'])
            features['deposit_to_borrow_ratio'] = features['deposit_count'] / max(1, features['borrow_count'])
            features['liquidation_rate'] = features['liquidation_count'] / features['total_transactions']
            
            # Risk indicators
            features['is_frequent_borrower'] = 1 if features['borrow_count'] > 5 else 0
            features['is_liquidated'] = 1 if features['liquidation_count'] > 0 else 0
            features['high_value_user'] = 1 if features['total_value_transacted'] > wallet_txns['value'].quantile(0.8) else 0
            
            # Engagement depth
            features['protocol_engagement_score'] = (
                features['unique_functions'] * 0.3 +
                min(features['total_transactions'] / 10, 5) * 0.4 +
                features['activity_span_days'] / 365 * 0.3
            )
            
            # Gas efficiency (proxy for sophistication)
            features['avg_gas_used'] = wallet_txns['gasUsed'].astype(float).mean()
            features['avg_gas_price'] = wallet_txns['gasPrice'].astype(float).mean()
            features['gas_efficiency'] = features['avg_gas_used'] / max(1, features['avg_gas_price'])
            
            # Behavioral consistency
            features['transaction_regularity'] = 1 / (1 + features['std_time_between_txns'] / 24)  # Normalize by 24 hours
            
            # Volume patterns
            features['value_consistency'] = 1 / (1 + features['std_transaction_value'] / max(1, features['avg_transaction_value']))
            
            wallet_features.append(features)
        
        feature_df = pd.DataFrame(wallet_features)
        
        # Handle missing values
        feature_df = feature_df.fillna(0)
        
        print(f"Engineered {len(feature_df.columns)-1} features for {len(feature_df)} wallets")
        return feature_df
    
    def create_composite_score(self, features_df):
        """
        Create a composite credit score using domain knowledge and unsupervised learning.
        
        The score combines multiple behavioral indicators weighted by their importance
        for assessing credit risk in DeFi protocols.
        """
        print("Creating composite credit scores...")
        
        # Prepare features for scoring (exclude wallet address)
        X = features_df.drop('wallet', axis=1)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Use clustering to identify behavioral patterns
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        # Define scoring components with weights
        scoring_components = {
            'repayment_behavior': 0.25,  # Most important for credit
            'consistency': 0.20,
            'engagement': 0.15,
            'risk_management': 0.15,
            'liquidity_provision': 0.10,
            'protocol_usage': 0.10,
            'no_liquidations': 0.05
        }
        
        scores = []
        
        for idx, row in features_df.iterrows():
            # Component scores (normalized 0-1)
            components = {}
            
            # Repayment behavior (higher repay/borrow ratio is better)
            components['repayment_behavior'] = min(1.0, row['repay_to_borrow_ratio'] / 2.0)
            
            # Consistency (regular transaction patterns)
            components['consistency'] = row['consistency_score']
            
            # Engagement (diverse protocol usage)
            components['engagement'] = min(1.0, row['protocol_engagement_score'] / 5.0)
            
            # Risk management (deposit/borrow ratio)
            components['risk_management'] = min(1.0, row['deposit_to_borrow_ratio'] / 3.0)
            
            # Liquidity provision (deposit activity)
            components['liquidity_provision'] = min(1.0, row['deposit_count'] / 10.0)
            
            # Protocol usage diversity
            components['protocol_usage'] = min(1.0, row['unique_functions'] / 5.0)
            
            # No liquidations bonus
            components['no_liquidations'] = 1.0 if row['liquidation_count'] == 0 else 0.0
            
            # Calculate weighted score
            weighted_score = sum(
                components[comp] * weight 
                for comp, weight in scoring_components.items()
            )
            
            # Apply cluster-based adjustment
            cluster_multipliers = {0: 1.2, 1: 1.0, 2: 0.8, 3: 0.9, 4: 1.1}
            cluster_adj = cluster_multipliers.get(clusters[idx], 1.0)
            
            # Final score (0-1000)
            final_score = weighted_score * cluster_adj * 1000
            final_score = max(0, min(1000, final_score))  # Clamp to valid range
            
            scores.append(final_score)
        
        features_df['credit_score'] = scores
        
        # Store results
        self.wallet_scores = dict(zip(features_df['wallet'], features_df['credit_score']))
        
        print(f"Generated credit scores for {len(features_df)} wallets")
        print(f"Score distribution: Min={min(scores):.1f}, Max={max(scores):.1f}, Mean={np.mean(scores):.1f}")
        
        return features_df
    
    def analyze_scores(self, scored_df):
        """
        Analyze the distribution and characteristics of credit scores.
        """
        print("Analyzing credit score distribution...")
        
        # Score ranges
        ranges = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500), 
                 (500, 600), (600, 700), (700, 800), (800, 900), (900, 1000)]
        
        range_analysis = {}
        
        for min_score, max_score in ranges:
            range_wallets = scored_df[
                (scored_df['credit_score'] >= min_score) & 
                (scored_df['credit_score'] < max_score)
            ]
            
            if len(range_wallets) > 0:
                range_analysis[f"{min_score}-{max_score}"] = {
                    'count': len(range_wallets),
                    'avg_transactions': range_wallets['total_transactions'].mean(),
                    'avg_repay_ratio': range_wallets['repay_to_borrow_ratio'].mean(),
                    'avg_liquidation_rate': range_wallets['liquidation_rate'].mean(),
                    'avg_engagement': range_wallets['protocol_engagement_score'].mean()
                }
        
        # Create visualizations
        self.create_visualizations(scored_df, range_analysis)
        
        return range_analysis
    
    def create_visualizations(self, scored_df, range_analysis):
        """Create visualizations for score analysis."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Score distribution histogram
        axes[0, 0].hist(scored_df['credit_score'], bins=50, alpha=0.7, color='skyblue')
        axes[0, 0].set_title('Credit Score Distribution')
        axes[0, 0].set_xlabel('Credit Score')
        axes[0, 0].set_ylabel('Number of Wallets')
        
        # Score ranges bar chart
        ranges = list(range_analysis.keys())
        counts = [range_analysis[r]['count'] for r in ranges]
        axes[0, 1].bar(ranges, counts, color='lightgreen')
        axes[0, 1].set_title('Wallets by Score Range')
        axes[0, 1].set_xlabel('Score Range')
        axes[0, 1].set_ylabel('Number of Wallets')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Score vs Transaction Count scatter
        axes[1, 0].scatter(scored_df['total_transactions'], scored_df['credit_score'], 
                          alpha=0.6, color='coral')
        axes[1, 0].set_title('Credit Score vs Transaction Count')
        axes[1, 0].set_xlabel('Total Transactions')
        axes[1, 0].set_ylabel('Credit Score')
        
        # Score vs Repayment Ratio scatter
        axes[1, 1].scatter(scored_df['repay_to_borrow_ratio'], scored_df['credit_score'], 
                          alpha=0.6, color='purple')
        axes[1, 1].set_title('Credit Score vs Repayment Ratio')
        axes[1, 1].set_xlabel('Repay to Borrow Ratio')
        axes[1, 1].set_ylabel('Credit Score')
        
        plt.tight_layout()
        plt.savefig('credit_score_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_results(self, scored_df, range_analysis):
        """Save results to files."""
        # Save wallet scores
        scored_df[['wallet', 'credit_score']].to_csv('wallet_credit_scores.csv', index=False)
        
        # Save detailed analysis
        with open('score_analysis.json', 'w') as f:
            json.dump(range_analysis, f, indent=2)
        
        print("Results saved to:")
        print("- wallet_credit_scores.csv")
        print("- score_analysis.json")
        print("- credit_score_analysis.png")
    
    def run_full_analysis(self, json_file_path):
        """Run the complete credit scoring analysis."""
        # Load data
        df = self.load_data(json_file_path)
        
        # Engineer features
        features_df = self.engineer_features(df)
        
        # Create credit scores
        scored_df = self.create_composite_score(features_df)
        
        # Analyze results
        range_analysis = self.analyze_scores(scored_df)
        
        # Save results
        self.save_results(scored_df, range_analysis)
        
        return scored_df, range_analysis

def main():
    """Main execution function."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python credit_scorer.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    
    # Initialize scorer
    scorer = DeFiCreditScorer()
    
    # Run analysis
    try:
        scored_df, analysis = scorer.run_full_analysis(json_file_path)
        
        print("\n" + "="*60)
        print("CREDIT SCORING ANALYSIS COMPLETE")
        print("="*60)
        
        print(f"\nProcessed {len(scored_df)} wallets")
        print(f"Average credit score: {scored_df['credit_score'].mean():.1f}")
        print(f"Score standard deviation: {scored_df['credit_score'].std():.1f}")
        
        # Show top and bottom performers
        print("\nTop 10 Credit Scores:")
        top_scores = scored_df.nlargest(10, 'credit_score')[['wallet', 'credit_score']]
        for _, row in top_scores.iterrows():
            print(f"  {row['wallet']}: {row['credit_score']:.1f}")
        
        print("\nBottom 10 Credit Scores:")
        bottom_scores = scored_df.nsmallest(10, 'credit_score')[['wallet', 'credit_score']]
        for _, row in bottom_scores.iterrows():
            print(f"  {row['wallet']}: {row['credit_score']:.1f}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
