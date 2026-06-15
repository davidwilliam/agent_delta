"""saasapp: a tiny layered multi-tenant service (AgentDelta hard-task fixture).

Layers: models -> storage -> policy -> service -> api. Authorization lives in the
policy layer; the service and api layers call into it.
"""

__version__ = "0.1.0"
