import json
import os

class RecommendationEngine:
    def __init__(self):
        self.strategies = self._load_strategies()
    
    def _load_strategies(self):
        """Load strategy data from JSON file or use default if file doesn't exist"""
        try:
            with open('data/launch_strategies.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default fallback strategies
            return {
                "launch_strategies": {
                    "new_product": {
                        "bootstrapped": {
                            "get_users": [
                                "Beta testing + early adopters program",
                                "Earned PR through founder story",
                                "High-impact partnerships with complementary products"
                            ],
                            "attract_investors": [
                                "Showcasing early user testimonials and traction",
                                "Targeted outreach to angel investors",
                                "Strategic industry events participation"
                            ]
                        },
                        "under_1m": {
                            "get_users": [
                                "Laser-focused ad campaigns on highest-converting channels",
                                "Content marketing highlighting problem solving",
                                "Referral program with compelling incentives"
                            ]
                        }
                    },
                    "rebrand": {
                        "series_a": {
                            "build_press": [
                                "Big media push with embargoed announcements",
                                "Paid influencer collaborations",
                                "High-end content storytelling across channels"
                            ]
                        }
                    }
                },
                "next_steps": {
                    "bootstrapped": [
                        "Focus on founder-led storytelling through podcasts and guest posts",
                        "Design a customer acquisition funnel with clear conversion points",
                        "Build a weekly content calendar that reinforces your unique value prop"
                    ],
                    "under_1m": [
                        "Run small test campaigns across 3 channels to identify highest ROI",
                        "Create investor-ready metrics dashboard showing key growth indicators",
                        "Develop case studies from your first 10 customers"
                    ],
                    "1m_3m": [
                        "Implement PR outreach strategy targeting tier 1 and industry publications",
                        "Build scalable growth experiments with clear success metrics",
                        "Create quarterly investor updates highlighting traction milestones"
                    ],
                    "3m_plus": [
                        "Launch category-defining thought leadership campaign",
                        "Plan high-visibility launch event",
                        "Implement influencer partnership program"
                    ]
                }
            }
    
    def get_strategies(self, launch_type, funding_status, primary_goal):
        """Get recommended strategies based on user inputs"""
        try:
            # Try to get specific recommendations based on the exact combination
            strategies = self.strategies["launch_strategies"][launch_type][funding_status][primary_goal]
            return strategies
        except KeyError:
            # Fallback to generic recommendations if the specific combination doesn't exist
            return [
                "Build a compelling founder story that highlights your unique perspective",
                "Create a waitlist or early access program to build anticipation",
                "Focus on one high-impact marketing channel rather than spreading thin"
            ]
    
    def get_next_steps(self, funding_status):
        """Get next steps based on funding status"""
        try:
            return self.strategies["next_steps"][funding_status]
        except KeyError:
            # Fallback
            return [
                "Focus on founder-led storytelling through podcasts and guest posts",
                "Design a customer acquisition funnel with clear conversion points",
                "Build a weekly content calendar that reinforces your unique value prop"
            ]