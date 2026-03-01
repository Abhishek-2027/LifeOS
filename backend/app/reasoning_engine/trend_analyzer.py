class TrendAnalyzer:

    def analyze(self, memories):

        return sorted(memories, key=lambda x: x.created_at)