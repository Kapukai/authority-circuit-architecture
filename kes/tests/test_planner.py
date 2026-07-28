import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"kes/scripts"))
from plan_capabilities import plan, validate_minimal

class PlannerTests(unittest.TestCase):
    def test_product_external_sensitive(self):
        wo={"id":"EDS-WO-0001","title":"Verified Decision","type":"product","risk":"high",
            "purpose":"Create one verified decision workflow.","acceptance_criteria":["DPR generated"],
            "deliverables":["web app"],"verification":["tests"],"release":{"human_approval":True},
            "external_deployment":True,"sensitive_data":True,"public_release":True}
        result=plan(wo)
        for c in ["architecture","product","engineering","security","verification","release","publisher","research"]:
            self.assertIn(c,result["required_capabilities"])
    def test_docs_are_lean(self):
        wo={"id":"KES-WO-0001","title":"Freeze KES","type":"documentation","risk":"low",
            "purpose":"Freeze the operating model for future work.","acceptance_criteria":["docs exist"],
            "deliverables":["constitution"],"verification":["file checks"],"release":{"human_approval":True}}
        self.assertEqual(plan(wo)["required_capabilities"],["architecture","verification"])
    def test_missing(self):
        self.assertTrue(validate_minimal({}))
if __name__=="__main__": unittest.main()
