# Annotation protocol

Each benchmark row represents one policy-instance unit:

`U = <file_id, resource_id, policy_sid>`

`consensus.csv` is the original project-team label set created from the
documented policy criteria. The reviewer-derived file is
`reviewer_consensus.csv`, generated from `expert_1.csv` and `expert_2.csv` by
`scripts/calculate_annotation_agreement.py`.

The two reviewer files contain 70 policy-instance labels each. They agree on
all 70 rows, producing a diagnostic Cohen's kappa of 1.0000. Because the
collection process was not documented as independent blinded annotation, this
value is retained for auditability but is not reported as inter-rater evidence
in the paper.
