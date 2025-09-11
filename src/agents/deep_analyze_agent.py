"""
Deep Analyze Agent for financial data analysis and valuation using SmolAgents
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from smolagents import Tool
from smolagents.memory import ConversationMemory
from smolagents.models import OpenAIModel

from .base_agent import BaseAgent, Task, TaskResult

logger = logging.getLogger(__name__)

class FinancialMetricsTool(Tool):
    """Tool for analyzing financial metrics"""
    
    def __init__(self):
        super().__init__(
            name="analyze_financial_metrics",
            description="Analyze financial metrics and performance indicators",
            parameters={
                "financial_data": {
                    "type": "array",
                    "description": "Array of financial data objects"
                },
                "metrics_to_analyze": {
                    "type": "array",
                    "description": "Specific metrics to focus on",
                    "items": {"type": "string"},
                    "default": ["revenue", "profit", "growth", "efficiency"]
                },
                "industry_context": {
                    "type": "string",
                    "description": "Industry context for analysis"
                }
            }
        )
    
    async def run(self, financial_data: List[Dict[str, Any]], metrics_to_analyze: List[str] = None, industry_context: str = None) -> Dict[str, Any]:
        """Analyze financial metrics"""
        try:
            if metrics_to_analyze is None:
                metrics_to_analyze = ["revenue", "profit", "growth", "efficiency"]
            
            analysis = {
                "metrics_analyzed": metrics_to_analyze,
                "data_points": len(financial_data),
                "key_findings": [],
                "trends": [],
                "anomalies": [],
                "recommendations": []
            }
            
            # Analyze each metric
            for metric in metrics_to_analyze:
                metric_analysis = await self._analyze_single_metric(financial_data, metric, industry_context)
                analysis["key_findings"].append(metric_analysis)
            
            # Identify trends
            analysis["trends"] = await self._identify_trends(financial_data, metrics_to_analyze)
            
            # Detect anomalies
            analysis["anomalies"] = await self._detect_anomalies(financial_data)
            
            # Generate recommendations
            analysis["recommendations"] = await self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Financial metrics analysis failed: {e}")
            return {"error": str(e)}
    
    async def _analyze_single_metric(self, data: List[Dict[str, Any]], metric: str, industry_context: str = None) -> Dict[str, Any]:
        """Analyze a single financial metric"""
        try:
            # Extract values for the metric
            values = []
            for item in data:
                if metric in item:
                    values.append(item[metric])
            
            if not values:
                return {"metric": metric, "error": "No data found for this metric"}
            
            # Basic statistical analysis
            avg_value = sum(values) / len(values)
            min_value = min(values)
            max_value = max(values)
            
            # Calculate growth if time series data
            growth_rates = []
            if len(values) > 1:
                for i in range(1, len(values)):
                    if values[i-1] != 0:
                        growth_rate = ((values[i] - values[i-1]) / values[i-1]) * 100
                        growth_rates.append(growth_rate)
            
            avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
            
            return {
                "metric": metric,
                "average": avg_value,
                "min": min_value,
                "max": max_value,
                "growth_rate": avg_growth,
                "volatility": max_value - min_value,
                "data_points": len(values),
                "industry_context": industry_context
            }
            
        except Exception as e:
            return {"metric": metric, "error": str(e)}
    
    async def _identify_trends(self, data: List[Dict[str, Any]], metrics: List[str]) -> List[Dict[str, Any]]:
        """Identify trends in financial data"""
        trends = []
        
        for metric in metrics:
            try:
                values = [item.get(metric, 0) for item in data if metric in item]
                if len(values) >= 3:
                    # Simple trend detection
                    first_half = values[:len(values)//2]
                    second_half = values[len(values)//2:]
                    
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)
                    
                    trend_direction = "increasing" if second_avg > first_avg else "decreasing"
                    trend_strength = abs(second_avg - first_avg) / first_avg if first_avg != 0 else 0
                    
                    trends.append({
                        "metric": metric,
                        "direction": trend_direction,
                        "strength": trend_strength,
                        "first_period_avg": first_avg,
                        "second_period_avg": second_avg
                    })
                    
            except Exception as e:
                logger.warning(f"Failed to analyze trend for {metric}: {e}")
        
        return trends
    
    async def _detect_anomalies(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in financial data"""
        anomalies = []
        
        try:
            # Get all numeric fields
            numeric_fields = set()
            for item in data:
                for key, value in item.items():
                    if isinstance(value, (int, float)):
                        numeric_fields.add(key)
            
            # Check for anomalies in each field
            for field in numeric_fields:
                values = [item[field] for item in data if field in item]
                if len(values) >= 5:
                    # Simple anomaly detection using standard deviation
                    avg = sum(values) / len(values)
                    variance = sum((x - avg) ** 2 for x in values) / len(values)
                    std_dev = variance ** 0.5
                    
                    # Find values more than 2 standard deviations from mean
                    for i, value in enumerate(values):
                        if abs(value - avg) > 2 * std_dev:
                            anomalies.append({
                                "field": field,
                                "value": value,
                                "expected_range": [avg - 2*std_dev, avg + 2*std_dev],
                                "deviation": abs(value - avg) / std_dev,
                                "data_point_index": i
                            })
                            
        except Exception as e:
            logger.warning(f"Anomaly detection failed: {e}")
        
        return anomalies
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        try:
            # Analyze trends for recommendations
            for trend in analysis.get("trends", []):
                if trend["direction"] == "decreasing" and trend["strength"] > 0.1:
                    recommendations.append(f"Consider investigating declining {trend['metric']} trend")
                elif trend["direction"] == "increasing" and trend["strength"] > 0.1:
                    recommendations.append(f"Positive {trend['metric']} trend identified - consider expanding in this area")
            
            # Analyze anomalies for recommendations
            if analysis.get("anomalies"):
                recommendations.append("Review detected anomalies for potential data quality issues")
            
            # Default recommendations
            if not recommendations:
                recommendations.append("Continue monitoring financial metrics regularly")
                recommendations.append("Consider benchmarking against industry standards")
                
        except Exception as e:
            logger.warning(f"Failed to generate recommendations: {e}")
            recommendations.append("Manual review recommended due to analysis limitations")
        
        return recommendations

class SentimentAnalysisTool(Tool):
    """Tool for sentiment analysis of financial text"""
    
    def __init__(self):
        super().__init__(
            name="analyze_sentiment",
            description="Analyze sentiment in financial text data",
            parameters={
                "texts": {
                    "type": "array",
                    "description": "Array of texts to analyze"
                },
                "context": {
                    "type": "string",
                    "description": "Context for sentiment analysis"
                }
            }
        )
    
    async def run(self, texts: List[str], context: str = None) -> Dict[str, Any]:
        """Analyze sentiment in financial texts"""
        try:
            if not texts:
                return {"error": "No texts provided for analysis"}
            
            analysis = {
                "total_texts": len(texts),
                "overall_sentiment": "neutral",
                "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
                "confidence": 0.0,
                "key_themes": [],
                "notable_quotes": []
            }
            
            # Simple keyword-based sentiment analysis
            positive_keywords = ["growth", "profit", "increase", "success", "strong", "positive", "opportunity"]
            negative_keywords = ["loss", "decline", "risk", "concern", "weak", "negative", "challenge"]
            
            sentiment_scores = []
            
            for i, text in enumerate(texts):
                text_lower = text.lower()
                
                # Calculate sentiment score
                positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
                negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
                
                if positive_count > negative_count:
                    sentiment = "positive"
                    score = positive_count / (positive_count + negative_count) if (positive_count + negative_count) > 0 else 0.5
                elif negative_count > positive_count:
                    sentiment = "negative"
                    score = -negative_count / (positive_count + negative_count) if (positive_count + negative_count) > 0 else -0.5
                else:
                    sentiment = "neutral"
                    score = 0.0
                
                sentiment_scores.append(score)
                analysis["sentiment_distribution"][sentiment] += 1
                
                # Store notable quotes
                if abs(score) > 0.3:
                    analysis["notable_quotes"].append({
                        "text": text[:200] + "..." if len(text) > 200 else text,
                        "sentiment": sentiment,
                        "score": score
                    })
            
            # Calculate overall sentiment
            if sentiment_scores:
                avg_score = sum(sentiment_scores) / len(sentiment_scores)
                if avg_score > 0.1:
                    analysis["overall_sentiment"] = "positive"
                elif avg_score < -0.1:
                    analysis["overall_sentiment"] = "negative"
                
                analysis["confidence"] = abs(avg_score)
            
            # Extract key themes
            analysis["key_themes"] = await self._extract_key_themes(texts)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {"error": str(e)}
    
    async def _extract_key_themes(self, texts: List[str]) -> List[str]:
        """Extract key themes from texts"""
        try:
            # Simple theme extraction using keyword frequency
            all_text = " ".join(texts).lower()
            
            financial_themes = [
                "revenue", "profit", "growth", "market", "investment", "risk",
                "technology", "innovation", "competition", "regulation", "economy"
            ]
            
            theme_counts = {}
            for theme in financial_themes:
                count = all_text.count(theme)
                if count > 0:
                    theme_counts[theme] = count
            
            # Return top themes
            sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
            return [theme for theme, count in sorted_themes[:5]]
            
        except Exception as e:
            logger.warning(f"Failed to extract key themes: {e}")
            return []

class ValuationTool(Tool):
    """Tool for financial valuation analysis"""
    
    def __init__(self):
        super().__init__(
            name="perform_valuation",
            description="Perform financial valuation analysis",
            parameters={
                "financial_data": {
                    "type": "object",
                    "description": "Financial data for valuation"
                },
                "valuation_method": {
                    "type": "string",
                    "description": "Valuation method to use",
                    "enum": ["dcf", "comparable", "multiples", "asset_based"],
                    "default": "multiples"
                },
                "industry": {
                    "type": "string",
                    "description": "Industry for context"
                }
            }
        )
    
    async def run(self, financial_data: Dict[str, Any], valuation_method: str = "multiples", industry: str = None) -> Dict[str, Any]:
        """Perform financial valuation"""
        try:
            valuation = {
                "method": valuation_method,
                "industry": industry,
                "inputs": financial_data,
                "assumptions": [],
                "valuation_result": None,
                "sensitivity_analysis": {}
            }
            
            if valuation_method == "multiples":
                valuation = await self._multiples_valuation(financial_data, industry)
            elif valuation_method == "dcf":
                valuation = await self._dcf_valuation(financial_data)
            elif valuation_method == "comparable":
                valuation = await self._comparable_valuation(financial_data, industry)
            elif valuation_method == "asset_based":
                valuation = await self._asset_based_valuation(financial_data)
            
            return valuation
            
        except Exception as e:
            logger.error(f"Valuation analysis failed: {e}")
            return {"error": str(e)}
    
    async def _multiples_valuation(self, data: Dict[str, Any], industry: str = None) -> Dict[str, Any]:
        """Perform multiples-based valuation"""
        try:
            # Industry multiples (simplified)
            industry_multiples = {
                "technology": {"pe": 25, "ps": 8, "ev_ebitda": 15},
                "finance": {"pe": 15, "ps": 3, "ev_ebitda": 10},
                "healthcare": {"pe": 20, "ps": 5, "ev_ebitda": 12},
                "consumer": {"pe": 18, "ps": 2, "ev_ebitda": 8}
            }
            
            multiples = industry_multiples.get(industry.lower(), {"pe": 18, "ps": 4, "ev_ebitda": 10})
            
            # Extract metrics from data
            net_income = data.get("net_income", 0)
            revenue = data.get("revenue", 0)
            ebitda = data.get("ebitda", 0)
            
            # Calculate valuations
            pe_valuation = net_income * multiples["pe"]
            ps_valuation = revenue * multiples["ps"]
            ev_ebitda_valuation = ebitda * multiples["ev_ebitda"]
            
            # Average valuation
            valuations = [pe_valuation, ps_valuation, ev_ebitda_valuation]
            valid_valuations = [v for v in valuations if v > 0]
            avg_valuation = sum(valid_valuations) / len(valid_valuations) if valid_valuations else 0
            
            return {
                "method": "multiples",
                "industry": industry,
                "multiples_used": multiples,
                "calculations": {
                    "pe_valuation": pe_valuation,
                    "ps_valuation": ps_valuation,
                    "ev_ebitda_valuation": ev_ebitda_valuation
                },
                "valuation_result": avg_valuation,
                "assumptions": [f"Used {industry} industry multiples" if industry else "Used generic multiples"]
            }
            
        except Exception as e:
            return {"method": "multiples", "error": str(e)}
    
    async def _dcf_valuation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform discounted cash flow valuation"""
        try:
            # Simplified DCF calculation
            fcf = data.get("free_cash_flow", 0)
            growth_rate = data.get("growth_rate", 0.05)
            discount_rate = data.get("discount_rate", 0.10)
            terminal_growth_rate = data.get("terminal_growth_rate", 0.02)
            
            # 5-year projection
            projected_fcfs = []
            for i in range(1, 6):
                projected_fcf = fcf * (1 + growth_rate) ** i
                projected_fcfs.append(projected_fcf)
            
            # Discount projected FCFs
            discounted_fcfs = []
            for i, fcf in enumerate(projected_fcfs, 1):
                discounted_fcf = fcf / ((1 + discount_rate) ** i)
                discounted_fcfs.append(discounted_fcf)
            
            # Terminal value
            terminal_fcf = projected_fcfs[-1] * (1 + terminal_growth_rate)
            terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
            discounted_terminal_value = terminal_value / ((1 + discount_rate) ** 5)
            
            # Total valuation
            total_valuation = sum(discounted_fcfs) + discounted_terminal_value
            
            return {
                "method": "dcf",
                "inputs": {
                    "initial_fcf": fcf,
                    "growth_rate": growth_rate,
                    "discount_rate": discount_rate,
                    "terminal_growth_rate": terminal_growth_rate
                },
                "projections": projected_fcfs,
                "discounted_cash_flows": discounted_fcfs,
                "terminal_value": terminal_value,
                "valuation_result": total_valuation,
                "assumptions": ["5-year projection", "perpetual growth model"]
            }
            
        except Exception as e:
            return {"method": "dcf", "error": str(e)}
    
    async def _comparable_valuation(self, data: Dict[str, Any], industry: str = None) -> Dict[str, Any]:
        """Perform comparable company analysis"""
        try:
            # Simplified comparable analysis
            metrics = {
                "revenue": data.get("revenue", 0),
                "net_income": data.get("net_income", 0),
                "assets": data.get("total_assets", 0)
            }
            
            # Mock comparable companies (in real implementation, this would come from market data)
            comparables = [
                {"name": "Company A", "multiple": 2.5, "metric": "revenue"},
                {"name": "Company B", "multiple": 15.0, "metric": "net_income"},
                {"name": "Company C", "multiple": 1.8, "metric": "assets"}
            ]
            
            valuations = []
            for comp in comparables:
                metric_value = metrics.get(comp["metric"], 0)
                valuation = metric_value * comp["multiple"]
                valuations.append(valuation)
            
            avg_valuation = sum(valuations) / len(valuations) if valuations else 0
            
            return {
                "method": "comparable",
                "industry": industry,
                "comparables": comparables,
                "individual_valuations": valuations,
                "valuation_result": avg_valuation,
                "assumptions": ["Limited comparable set", "Market-based multiples"]
            }
            
        except Exception as e:
            return {"method": "comparable", "error": str(e)}
    
    async def _asset_based_valuation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform asset-based valuation"""
        try:
            total_assets = data.get("total_assets", 0)
            total_liabilities = data.get("total_liabilities", 0)
            intangible_assets = data.get("intangible_assets", 0)
            
            # Book value
            book_value = total_assets - total_liabilities
            
            # Adjusted book value (excluding intangibles)
            adjusted_book_value = book_value - intangible_assets
            
            # Use average of book value and adjusted book value
            valuation = (book_value + adjusted_book_value) / 2
            
            return {
                "method": "asset_based",
                "inputs": {
                    "total_assets": total_assets,
                    "total_liabilities": total_liabilities,
                    "intangible_assets": intangible_assets
                },
                "calculations": {
                    "book_value": book_value,
                    "adjusted_book_value": adjusted_book_value
                },
                "valuation_result": valuation,
                "assumptions": ["Conservative valuation", "Asset-focused approach"]
            }
            
        except Exception as e:
            return {"method": "asset_based", "error": str(e)}

class RiskAssessmentTool(Tool):
    """Tool for risk assessment"""
    
    def __init__(self):
        super().__init__(
            name="assess_risks",
            description="Assess financial and business risks",
            parameters={
                "data": {
                    "type": "object",
                    "description": "Data for risk assessment"
                },
                "risk_categories": {
                    "type": "array",
                    "description": "Risk categories to assess",
                    "items": {"type": "string"},
                    "default": ["financial", "operational", "market", "regulatory"]
                }
            }
        )
    
    async def run(self, data: Dict[str, Any], risk_categories: List[str] = None) -> Dict[str, Any]:
        """Assess risks based on data"""
        try:
            if risk_categories is None:
                risk_categories = ["financial", "operational", "market", "regulatory"]
            
            assessment = {
                "risk_categories": risk_categories,
                "overall_risk_level": "medium",
                "risk_scores": {},
                "risk_factors": [],
                "mitigation_strategies": []
            }
            
            # Assess each risk category
            total_score = 0
            for category in risk_categories:
                category_score = await self._assess_risk_category(data, category)
                assessment["risk_scores"][category] = category_score
                total_score += category_score
            
            # Calculate overall risk level
            avg_score = total_score / len(risk_categories) if risk_categories else 0
            if avg_score > 0.7:
                assessment["overall_risk_level"] = "high"
            elif avg_score > 0.4:
                assessment["overall_risk_level"] = "medium"
            else:
                assessment["overall_risk_level"] = "low"
            
            # Generate risk factors
            assessment["risk_factors"] = await self._identify_risk_factors(data, risk_categories)
            
            # Generate mitigation strategies
            assessment["mitigation_strategies"] = await self._generate_mitigation_strategies(assessment)
            
            return assessment
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return {"error": str(e)}
    
    async def _assess_risk_category(self, data: Dict[str, Any], category: str) -> float:
        """Assess risk for a specific category"""
        try:
            if category == "financial":
                return await self._assess_financial_risk(data)
            elif category == "operational":
                return await self._assess_operational_risk(data)
            elif category == "market":
                return await self._assess_market_risk(data)
            elif category == "regulatory":
                return await self._assess_regulatory_risk(data)
            else:
                return 0.5  # Default medium risk
                
        except Exception as e:
            logger.warning(f"Failed to assess {category} risk: {e}")
            return 0.5
    
    async def _assess_financial_risk(self, data: Dict[str, Any]) -> float:
        """Assess financial risk"""
        try:
            # Simple financial risk assessment
            debt_to_equity = data.get("debt_to_equity", 0)
            current_ratio = data.get("current_ratio", 1.0)
            profit_margin = data.get("profit_margin", 0)
            
            risk_score = 0.0
            
            # High debt increases risk
            if debt_to_equity > 2.0:
                risk_score += 0.3
            elif debt_to_equity > 1.0:
                risk_score += 0.15
            
            # Low liquidity increases risk
            if current_ratio < 1.0:
                risk_score += 0.3
            elif current_ratio < 1.5:
                risk_score += 0.15
            
            # Low profitability increases risk
            if profit_margin < 0:
                risk_score += 0.4
            elif profit_margin < 0.05:
                risk_score += 0.2
            
            return min(risk_score, 1.0)
            
        except Exception as e:
            logger.warning(f"Financial risk assessment failed: {e}")
            return 0.5
    
    async def _assess_operational_risk(self, data: Dict[str, Any]) -> float:
        """Assess operational risk"""
        try:
            # Simplified operational risk assessment
            operational_efficiency = data.get("operational_efficiency", 0.7)
            employee_turnover = data.get("employee_turnover", 0.15)
            
            risk_score = 0.0
            
            if operational_efficiency < 0.5:
                risk_score += 0.3
            elif operational_efficiency < 0.7:
                risk_score += 0.15
            
            if employee_turnover > 0.25:
                risk_score += 0.2
            elif employee_turnover > 0.15:
                risk_score += 0.1
            
            return min(risk_score, 1.0)
            
        except Exception as e:
            logger.warning(f"Operational risk assessment failed: {e}")
            return 0.5
    
    async def _assess_market_risk(self, data: Dict[str, Any]) -> float:
        """Assess market risk"""
        try:
            # Simplified market risk assessment
            market_volatility = data.get("market_volatility", 0.2)
            competitive_pressure = data.get("competitive_pressure", 0.5)
            
            risk_score = (market_volatility * 0.6) + (competitive_pressure * 0.4)
            return min(risk_score, 1.0)
            
        except Exception as e:
            logger.warning(f"Market risk assessment failed: {e}")
            return 0.5
    
    async def _assess_regulatory_risk(self, data: Dict[str, Any]) -> float:
        """Assess regulatory risk"""
        try:
            # Simplified regulatory risk assessment
            regulatory_changes = data.get("regulatory_changes", "low")
            
            if regulatory_changes == "high":
                return 0.8
            elif regulatory_changes == "medium":
                return 0.5
            else:
                return 0.2
                
        except Exception as e:
            logger.warning(f"Regulatory risk assessment failed: {e}")
            return 0.5
    
    async def _identify_risk_factors(self, data: Dict[str, Any], categories: List[str]) -> List[Dict[str, Any]]:
        """Identify specific risk factors"""
        risk_factors = []
        
        try:
            # Financial risk factors
            if "financial" in categories:
                debt_to_equity = data.get("debt_to_equity", 0)
                if debt_to_equity > 2.0:
                    risk_factors.append({
                        "category": "financial",
                        "factor": "High debt-to-equity ratio",
                        "severity": "high",
                        "description": f"Debt-to-equity ratio of {debt_to_equity} indicates high financial leverage"
                    })
            
            # Operational risk factors
            if "operational" in categories:
                efficiency = data.get("operational_efficiency", 0.7)
                if efficiency < 0.5:
                    risk_factors.append({
                        "category": "operational",
                        "factor": "Low operational efficiency",
                        "severity": "medium",
                        "description": f"Operational efficiency of {efficiency} indicates process inefficiencies"
                    })
            
        except Exception as e:
            logger.warning(f"Risk factor identification failed: {e}")
        
        return risk_factors
    
    async def _generate_mitigation_strategies(self, assessment: Dict[str, Any]) -> List[str]:
        """Generate risk mitigation strategies"""
        strategies = []
        
        try:
            risk_level = assessment.get("overall_risk_level", "medium")
            
            if risk_level == "high":
                strategies.append("Implement comprehensive risk management framework")
                strategies.append("Regular monitoring and reporting of key risk indicators")
                strategies.append("Diversification strategies to reduce concentration risk")
            elif risk_level == "medium":
                strategies.append("Enhanced monitoring of identified risk areas")
                strategies.append("Develop contingency plans for key risks")
            else:
                strategies.append("Maintain current risk management practices")
                strategies.append("Periodic risk assessment review")
            
        except Exception as e:
            logger.warning(f"Mitigation strategy generation failed: {e}")
            strategies.append("Review risk management approach")
        
        return strategies

class DeepAnalyzeAgent(BaseAgent):
    """Agent for deep analysis of financial data and content using SmolAgents"""
    
    def __init__(self, model: OpenAIModel, memory: ConversationMemory = None):
        super().__init__(
            name="DeepAnalyzeAgent",
            model=model,
            memory=memory or ConversationMemory()
        )
        
        # Add analysis tools
        self.add_custom_tool(FinancialMetricsTool())
        self.add_custom_tool(SentimentAnalysisTool())
        self.add_custom_tool(ValuationTool())
        self.add_custom_tool(RiskAssessmentTool())
    
    async def execute_task(self, task: Task) -> TaskResult:
        """Execute deep analysis tasks using SmolAgents"""
        start_time = datetime.now()
        
        try:
            analysis_type = task.parameters.get("analysis_type")
            data = task.parameters.get("data")
            context = task.parameters.get("context", {})
            
            if not analysis_type or not data:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    error="Analysis type and data are required"
                )
            
            # Create task description for SmolAgents
            task_description = f"Perform {analysis_type} analysis on financial data"
            
            # Use SmolAgents to orchestrate the analysis
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                analysis_result = result.get("result", {})
                
                # Enhance with specific analysis
                enhanced_result = await self._enhance_analysis_result(analysis_result, task)
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=enhanced_result,
                    execution_time=execution_time,
                    metadata={
                        "analysis_type": analysis_type,
                        "data_points": len(data) if isinstance(data, list) else 1,
                        "method": "smolagents"
                    }
                )
            else:
                # Fallback to traditional method
                fallback_result = await self._execute_traditional_analysis(task)
                fallback_result.execution_time = (datetime.now() - start_time).total_seconds()
                return fallback_result
                
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    async def _enhance_analysis_result(self, smolagents_result: Dict[str, Any], task: Task) -> Dict[str, Any]:
        """Enhance SmolAgents result with specific analysis tools"""
        try:
            analysis_type = task.parameters.get("analysis_type")
            data = task.parameters.get("data")
            context = task.parameters.get("context", {})
            
            # Apply specific analysis based on type
            if analysis_type == "financial_metrics":
                metrics_tool = FinancialMetricsTool()
                metrics_result = await metrics_tool.run(data, context.get("metrics_to_analyze"))
                smolagents_result.update(metrics_result)
            
            elif analysis_type == "sentiment_analysis":
                sentiment_tool = SentimentAnalysisTool()
                sentiment_result = await sentiment_tool.run(data, context.get("analysis_context"))
                smolagents_result.update(sentiment_result)
            
            elif analysis_type == "valuation":
                valuation_tool = ValuationTool()
                valuation_result = await valuation_tool.run(data, context.get("valuation_method"), context.get("industry"))
                smolagents_result.update(valuation_result)
            
            elif analysis_type == "risk_assessment":
                risk_tool = RiskAssessmentTool()
                risk_result = await risk_tool.run(data, context.get("risk_categories"))
                smolagents_result.update(risk_result)
            
            # Add metadata
            smolagents_result["enhanced_at"] = datetime.now().isoformat()
            smolagents_result["enhanced_by"] = "DeepAnalyzeAgent"
            
            return smolagents_result
            
        except Exception as e:
            logger.error(f"Failed to enhance analysis result: {e}")
            return smolagents_result
    
    async def _execute_traditional_analysis(self, task: Task) -> TaskResult:
        """Fallback traditional analysis execution"""
        try:
            analysis_type = task.parameters.get("analysis_type")
            data = task.parameters.get("data")
            context = task.parameters.get("context", {})
            
            if analysis_type == "financial_metrics":
                result = await self._analyze_financial_metrics(data, context)
            elif analysis_type == "sentiment_analysis":
                result = await self._analyze_sentiment(data, context)
            elif analysis_type == "trend_analysis":
                result = await self._analyze_trends(data, context)
            elif analysis_type == "risk_assessment":
                result = await self._assess_risks(data, context)
            elif analysis_type == "comparative_analysis":
                result = await self._comparative_analysis(data, context)
            else:
                result = {"error": f"Unknown analysis type: {analysis_type}"}
            
            return TaskResult(
                task_id=task.id,
                success="error" not in result,
                result=result if "error" not in result else None,
                error=result.get("error") if "error" in result else None,
                metadata={
                    "analysis_type": analysis_type,
                    "data_points": len(data) if isinstance(data, list) else 1,
                    "method": "traditional"
                }
            )
            
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e)
            )
    
    async def _analyze_financial_metrics(self, data: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial metrics"""
        try:
            metrics_tool = FinancialMetricsTool()
            return await metrics_tool.run(data, context.get("metrics_to_analyze"), context.get("industry_context"))
        except Exception as e:
            return {"error": f"Financial metrics analysis failed: {str(e)}"}
    
    async def _analyze_sentiment(self, data: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment from text data"""
        try:
            sentiment_tool = SentimentAnalysisTool()
            return await sentiment_tool.run(data, context.get("analysis_context"))
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    async def _analyze_trends(self, data: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in time series data"""
        try:
            # Simple trend analysis
            trends = []
            for key, values in data.items():
                if isinstance(values, list) and len(values) > 1:
                    trend = "increasing" if values[-1] > values[0] else "decreasing"
                    trends.append({"metric": key, "trend": trend, "values": values})
            
            return {"trends": trends, "analysis_context": context}
        except Exception as e:
            return {"error": f"Trend analysis failed: {str(e)}"}
    
    async def _assess_risks(self, data: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks based on data"""
        try:
            risk_tool = RiskAssessmentTool()
            return await risk_tool.run(data, context.get("risk_categories"))
        except Exception as e:
            return {"error": f"Risk assessment failed: {str(e)}"}
    
    async def _comparative_analysis(self, data: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comparative analysis between multiple entities"""
        try:
            # Simple comparative analysis
            comparison = {
                "entities": [],
                "metrics": {},
                "rankings": {}
            }
            
            for entity in data:
                entity_name = entity.get("name", "Unknown")
                comparison["entities"].append(entity_name)
                
                for key, value in entity.items():
                    if key != "name" and isinstance(value, (int, float)):
                        if key not in comparison["metrics"]:
                            comparison["metrics"][key] = []
                        comparison["metrics"][key].append({"entity": entity_name, "value": value})
            
            # Generate rankings
            for metric, values in comparison["metrics"].items():
                sorted_values = sorted(values, key=lambda x: x["value"], reverse=True)
                comparison["rankings"][metric] = [item["entity"] for item in sorted_values]
            
            return comparison
            
        except Exception as e:
            return {"error": f"Comparative analysis failed: {str(e)}"}
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        return [
            "financial_metrics_analysis",
            "sentiment_analysis",
            "trend_analysis",
            "risk_assessment",
            "comparative_analysis",
            "valuation_analysis",
            "data_visualization",
            "smolagents_integration"
        ]
    
    async def analyze_with_smolagents(self, data: Any, analysis_type: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform analysis using SmolAgents framework directly"""
        try:
            # Create comprehensive analysis task
            task_description = f"""
            Perform comprehensive {analysis_type} analysis on the provided data.
            
            Analysis type: {analysis_type}
            Data context: {context or 'General financial analysis'}
            
            Please provide:
            1. Detailed analysis results
            2. Key insights and findings
            3. Visualizations recommendations
            4. Actionable recommendations
            5. Risk assessments if applicable
            """
            
            result = await self.run_task_with_smolagents(task_description)
            
            if result.get("success"):
                return result.get("result", {})
            else:
                raise Exception(f"SmolAgents analysis failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"SmolAgents analysis failed: {e}")
            raise