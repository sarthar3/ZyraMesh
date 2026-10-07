import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class DataProvider(ABC):
    """Abstract Data-as-a-Service (DaaS) Provider Interface."""
    
    @abstractmethod
    async def search(self, query: str, max_budget: Optional[float] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_item(self, product_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_price(self, product_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_reviews(self, product_id: str) -> Dict[str, Any]:
        pass


class MockDataProvider(DataProvider):
    """
    Mock & JSON Data Provider supporting the Flagship Laptop Shopping Domain.
    Returns structured product specs, prices, and reviews clearly tagged with data provenance.
    """
    MOCK_CATALOG = [
        {
            "product_id": "laptop_001",
            "name": "Lenovo Legion Slim 5",
            "brand": "Lenovo",
            "price": 68990.0,
            "currency": "INR",
            "source": "Local DaaS Catalog",
            "timestamp": "2026-09-12T00:00:00Z",
            "data_mode": "MOCK",
            "specifications": {
                "cpu": "AMD Ryzen 7 7840HS",
                "gpu": "NVIDIA RTX 4060 8GB VRAM",
                "ram": "16GB DDR5",
                "storage": "512GB NVMe SSD",
                "display": "16-inch WQXGA 165Hz",
                "battery": "80Whr"
            },
            "rating": 4.6,
            "reviews_count": 340,
            "reviews": [
                {"user": "AI_Dev_Rahul", "rating": 5, "comment": "Runs PyTorch CUDA models smoothly. Great thermals."},
                {"user": "TechReviewer", "rating": 4, "comment": "Solid build quality and GPU VRAM for local LLM inference."}
            ],
            "availability": "IN_STOCK"
        },
        {
            "product_id": "laptop_002",
            "name": "ASUS TUF Gaming F15",
            "brand": "ASUS",
            "price": 64990.0,
            "currency": "INR",
            "source": "Local DaaS Catalog",
            "timestamp": "2026-09-12T00:00:00Z",
            "data_mode": "MOCK",
            "specifications": {
                "cpu": "Intel Core i7-12700H",
                "gpu": "NVIDIA RTX 4050 6GB VRAM",
                "ram": "16GB DDR5",
                "storage": "1TB NVMe SSD",
                "display": "15.6-inch FHD 144Hz",
                "battery": "90Whr"
            },
            "rating": 4.4,
            "reviews_count": 520,
            "reviews": [
                {"user": "StudentCoder", "rating": 4, "comment": "Good budget option for ML datasets and heavy multitasking."},
                {"user": "Gamer123", "rating": 5, "comment": "Fast SSD and 90Whr battery lasts long."}
            ],
            "availability": "IN_STOCK"
        },
        {
            "product_id": "laptop_003",
            "name": "Acer Nitro V 16",
            "brand": "Acer",
            "price": 72990.0,
            "currency": "INR",
            "source": "Local DaaS Catalog",
            "timestamp": "2026-09-12T00:00:00Z",
            "data_mode": "MOCK",
            "specifications": {
                "cpu": "AMD Ryzen 7 8845HS",
                "gpu": "NVIDIA RTX 4060 8GB VRAM",
                "ram": "16GB DDR5",
                "storage": "1TB NVMe SSD",
                "display": "16-inch WUXGA 165Hz",
                "battery": "57Whr"
            },
            "rating": 4.3,
            "reviews_count": 180,
            "reviews": [
                {"user": "DataScientist_M", "rating": 4, "comment": "High performance Ryzen 8000 CPU with dedicated NPU."}
            ],
            "availability": "IN_STOCK"
        }
    ]

    async def search(self, query: str, max_budget: Optional[float] = None) -> List[Dict[str, Any]]:
        results = []
        for item in self.MOCK_CATALOG:
            if max_budget is not None and item["price"] > max_budget:
                continue
            results.append(item)
        return results

    async def get_item(self, product_id: str) -> Optional[Dict[str, Any]]:
        for item in self.MOCK_CATALOG:
            if item["product_id"] == product_id:
                return item
        return None

    async def get_price(self, product_id: str) -> Dict[str, Any]:
        item = await self.get_item(product_id)
        if item:
            return {"price": item["price"], "currency": item["currency"], "data_mode": item["data_mode"]}
        return {"price": 0.0, "currency": "INR", "data_mode": "MOCK"}

    async def get_reviews(self, product_id: str) -> Dict[str, Any]:
        item = await self.get_item(product_id)
        if item:
            return {"rating": item["rating"], "reviews": item["reviews"], "data_mode": item["data_mode"]}
        return {"rating": 0.0, "reviews": [], "data_mode": "MOCK"}
