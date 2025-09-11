import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class ChartGenerator:
    """Generate charts for HTML reports"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def generate_chart(self, chart_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Chart.js configuration for a chart"""
        try:
            chart_type = chart_data.get("type", "line")
            chart_id = chart_data.get("id", f"chart_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            
            if chart_type == "line":
                config = await self._generate_line_chart(chart_data)
            elif chart_type == "bar":
                config = await self._generate_bar_chart(chart_data)
            elif chart_type == "pie":
                config = await self._generate_pie_chart(chart_data)
            elif chart_type == "doughnut":
                config = await self._generate_doughnut_chart(chart_data)
            elif chart_type == "radar":
                config = await self._generate_radar_chart(chart_data)
            elif chart_type == "scatter":
                config = await self._generate_scatter_chart(chart_data)
            elif chart_type == "area":
                config = await self._generate_area_chart(chart_data)
            elif chart_type == "heatmap":
                config = await self._generate_heatmap_chart(chart_data)
            else:
                config = await self._generate_line_chart(chart_data)  # Default to line chart
            
            return {
                "success": True,
                "config": config,
                "chart_type": chart_type,
                "chart_id": chart_id
            }
            
        except Exception as e:
            logger.error(f"Failed to generate chart: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_line_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate line chart configuration"""
        datasets = data.get("datasets", [])
        labels = data.get("labels", [])
        
        # Process datasets
        processed_datasets = []
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
        
        for i, dataset in enumerate(datasets):
            color = colors[i % len(colors)]
            processed_dataset = {
                "label": dataset.get("label", f"Dataset {i+1}"),
                "data": dataset.get("data", []),
                "borderColor": color,
                "backgroundColor": color + "20",  # Add transparency
                "borderWidth": 2,
                "fill": False,
                "tension": 0.4
            }
            
            # Add additional styling options
            if dataset.get("fill"):
                processed_dataset["fill"] = dataset["fill"]
            if dataset.get("pointRadius"):
                processed_dataset["pointRadius"] = dataset["pointRadius"]
            if dataset.get("pointHoverRadius"):
                processed_dataset["pointHoverRadius"] = dataset["pointHoverRadius"]
            
            processed_datasets.append(processed_dataset)
        
        return {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": processed_datasets
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    },
                    "legend": {
                        "display": True,
                        "position": "top"
                    },
                    "tooltip": {
                        "mode": "index",
                        "intersect": False
                    }
                },
                "scales": {
                    "x": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("x_axis_label", "X Axis")
                        }
                    },
                    "y": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("y_axis_label", "Y Axis")
                        }
                    }
                },
                "interaction": {
                    "mode": "nearest",
                    "axis": "x",
                    "intersect": False
                }
            }
        }
    
    async def _generate_bar_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate bar chart configuration"""
        datasets = data.get("datasets", [])
        labels = data.get("labels", [])
        
        # Process datasets
        processed_datasets = []
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
        
        for i, dataset in enumerate(datasets):
            color = colors[i % len(colors)]
            processed_dataset = {
                "label": dataset.get("label", f"Dataset {i+1}"),
                "data": dataset.get("data", []),
                "backgroundColor": color,
                "borderColor": color,
                "borderWidth": 1
            }
            
            processed_datasets.append(processed_dataset)
        
        return {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": processed_datasets
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    },
                    "legend": {
                        "display": True,
                        "position": "top"
                    }
                },
                "scales": {
                    "x": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("x_axis_label", "X Axis")
                        }
                    },
                    "y": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("y_axis_label", "Y Axis")
                        },
                        "beginAtZero": True
                    }
                }
            }
        }
    
    async def _generate_pie_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pie chart configuration"""
        labels = data.get("labels", [])
        values = data.get("values", [])
        
        colors = [
            '#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', 
            '#00f2fe', '#43e97b', '#38f9d7', '#ffecd2', '#fcb69f'
        ]
        
        return {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [{
                    "data": values,
                    "backgroundColor": colors[:len(labels)],
                    "borderColor": "#fff",
                    "borderWidth": 2
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    },
                    "legend": {
                        "display": True,
                        "position": "right"
                    },
                    "tooltip": {
                        "callbacks": {
                            "label": "function(context) { return context.label + ': ' + context.parsed + '%'; }"
                        }
                    }
                }
            }
        }
    
    async def _generate_doughnut_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate doughnut chart configuration"""
        labels = data.get("labels", [])
        values = data.get("values", [])
        
        colors = [
            '#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', 
            '#00f2fe', '#43e97b', '#38f9d7', '#ffecd2', '#fcb69f'
        ]
        
        return {
            "type": "doughnut",
            "data": {
                "labels": labels,
                "datasets": [{
                    "data": values,
                    "backgroundColor": colors[:len(labels)],
                    "borderColor": "#fff",
                    "borderWidth": 2
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    },
                    "legend": {
                        "display": True,
                        "position": "right"
                    }
                },
                "cutout": "50%"
            }
        }
    
    async def _generate_radar_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate radar chart configuration"""
        datasets = data.get("datasets", [])
        labels = data.get("labels", [])
        
        processed_datasets = []
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
        
        for i, dataset in enumerate(datasets):
            color = colors[i % len(colors)]
            processed_dataset = {
                "label": dataset.get("label", f"Dataset {i+1}"),
                "data": dataset.get("data", []),
                "borderColor": color,
                "backgroundColor": color + "40",
                "pointBackgroundColor": color,
                "pointBorderColor": "#fff",
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": color
            }
            processed_datasets.append(processed_dataset)
        
        return {
            "type": "radar",
            "data": {
                "labels": labels,
                "datasets": processed_datasets
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    }
                },
                "scales": {
                    "r": {
                        "beginAtZero": True,
                        "ticks": {
                            "stepSize": 20
                        }
                    }
                }
            }
        }
    
    async def _generate_scatter_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate scatter chart configuration"""
        datasets = data.get("datasets", [])
        
        processed_datasets = []
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
        
        for i, dataset in enumerate(datasets):
            color = colors[i % len(colors)]
            processed_dataset = {
                "label": dataset.get("label", f"Dataset {i+1}"),
                "data": dataset.get("data", []),
                "backgroundColor": color,
                "borderColor": color,
                "pointRadius": 6,
                "pointHoverRadius": 8
            }
            processed_datasets.append(processed_dataset)
        
        return {
            "type": "scatter",
            "data": {
                "datasets": processed_datasets
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    }
                },
                "scales": {
                    "x": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("x_axis_label", "X Axis")
                        },
                        "type": "linear",
                        "position": "bottom"
                    },
                    "y": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("y_axis_label", "Y Axis")
                        }
                    }
                }
            }
        }
    
    async def _generate_area_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate area chart (filled line chart) configuration"""
        config = await self._generate_line_chart(data)
        config["data"]["datasets"][0]["fill"] = True
        return config
    
    async def _generate_heatmap_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate heatmap chart configuration"""
        # For heatmap, we'll use a scatter chart with point styling
        heatmap_data = data.get("heatmap_data", [])
        
        processed_data = []
        for point in heatmap_data:
            processed_data.append({
                "x": point.get("x", 0),
                "y": point.get("y", 0),
                "r": point.get("value", 1) * 3  # Scale radius by value
            })
        
        return {
            "type": "bubble",
            "data": {
                "datasets": [{
                    "label": data.get("title", "Heatmap"),
                    "data": processed_data,
                    "backgroundColor": "rgba(102, 126, 234, 0.6)",
                    "borderColor": "rgba(102, 126, 234, 1)",
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", ""),
                        "font": {"size": 16, "weight": "bold"}
                    }
                },
                "scales": {
                    "x": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("x_axis_label", "X Axis")
                        }
                    },
                    "y": {
                        "display": True,
                        "title": {
                            "display": True,
                            "text": data.get("y_axis_label", "Y Axis")
                        }
                    }
                }
            }
        }
    
    async def generate_financial_chart(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specialized financial charts"""
        chart_type = financial_data.get("financial_chart_type", "candlestick")
        
        if chart_type == "candlestick":
            return await self._generate_candlestick_chart(financial_data)
        elif chart_type == "volume":
            return await self._generate_volume_chart(financial_data)
        elif chart_type == "portfolio":
            return await self._generate_portfolio_chart(financial_data)
        else:
            return await self._generate_line_chart(financial_data)
    
    async def _generate_candlestick_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate candlestick chart (simulated with multiple datasets)"""
        ohlc_data = data.get("ohlc_data", [])
        labels = [point.get("date", "") for point in ohlc_data]
        
        # Create separate datasets for high, low, open, close
        high_data = [point.get("high", 0) for point in ohlc_data]
        low_data = [point.get("low", 0) for point in ohlc_data]
        open_data = [point.get("open", 0) for point in ohlc_data]
        close_data = [point.get("close", 0) for point in ohlc_data]
        
        return {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "High",
                        "data": high_data,
                        "borderColor": "#4caf50",
                        "backgroundColor": "rgba(76, 175, 80, 0.1)",
                        "fill": "+1"
                    },
                    {
                        "label": "Low",
                        "data": low_data,
                        "borderColor": "#f44336",
                        "backgroundColor": "rgba(244, 67, 54, 0.1)",
                        "fill": "-1"
                    },
                    {
                        "label": "Close",
                        "data": close_data,
                        "borderColor": "#2196f3",
                        "backgroundColor": "transparent",
                        "borderWidth": 3
                    }
                ]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", "Price Chart"),
                        "font": {"size": 16, "weight": "bold"}
                    }
                },
                "scales": {
                    "x": {
                        "display": True,
                        "title": {"display": True, "text": "Date"}
                    },
                    "y": {
                        "display": True,
                        "title": {"display": True, "text": "Price"}
                    }
                }
            }
        }
    
    async def _generate_volume_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate volume chart"""
        volume_data = data.get("volume_data", [])
        labels = [point.get("date", "") for point in volume_data]
        volumes = [point.get("volume", 0) for point in volume_data]
        
        return {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Volume",
                    "data": volumes,
                    "backgroundColor": "#667eea",
                    "borderColor": "#667eea"
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": data.get("title", "Volume Chart"),
                        "font": {"size": 16, "weight": "bold"}
                    }
                },
                "scales": {
                    "x": {
                        "display": True,
                        "title": {"display": True, "text": "Date"}
                    },
                    "y": {
                        "display": True,
                        "title": {"display": True, "text": "Volume"}
                    }
                }
            }
        }
    
    async def _generate_portfolio_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate portfolio allocation chart"""
        allocations = data.get("allocations", [])
        labels = [item.get("asset", "") for item in allocations]
        values = [item.get("percentage", 0) for item in allocations]
        
        return await self._generate_doughnut_chart({
            "title": data.get("title", "Portfolio Allocation"),
            "labels": labels,
            "values": values
        })