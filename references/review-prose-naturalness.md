# Natural prose in review articles

Use this reference when a review, perspective, or discussion reads as if it is
describing its own editorial machinery instead of discussing the science.

## Keep the editorial scaffolding backstage

Claim ledgers, source locks, evidence cards, evidence chains, section contracts,
comparison frameworks, synthesis units, and reviewer gates are editorial tools.
They help the writer think, but their labels should not automatically appear in
the manuscript. A finished paragraph should normally discuss a material, model,
measurement, experiment, comparison, limitation, or inference.

Run an object-level pass before delivery:

1. Underline the grammatical subject of each sentence.
2. Mark subjects that refer to the manuscript or its editing machinery, such as
   `this Review`, `the framework`, `the evidence`, `the landscape`, `the axis`,
   `the pipeline`, `the narrative`, `本文`, `框架`, `证据链`, `图谱`, or `维度`.
3. Keep self-reference when it is needed to state scope, methods, or an original
   taxonomy. Else name the study, material, model, experiment, or result that is
   doing the scientific work.
4. Replace the abstract label with the actual relation: comparison, failed
   transfer, prospective validation, missing control, restricted domain, or
   decision consequence.
5. Read the paragraph without its citations. It should still make a concrete and
   testable statement rather than merely announce that synthesis occurred.

## Run a clean-manuscript gate

Review the submission artifact separately from the author-facing handoff. Check
every reader-visible component, including headings, shaded callouts, text boxes,
table cells, figure labels, captions, footnotes, endnotes, and supplementary
prose. A polished box is still leakage when its function is to instruct the
author or record an editor's analysis.

| Candidate | Reader-visible decision |
|---|---|
| `中心判断`, `Editorial assessment`, or another analysis label | Move the judgment to the author decision log; rewrite the underlying scientific point directly when it belongs in the paper. |
| `作者提示`, `Note to author`, revision instructions, or unresolved questions | Resolve it, move it to comments/track changes when requested, or list it in the handoff; do not retain it as manuscript prose. |
| `TODO`, `citation needed`, `insert value`, model/agent instructions, or output labels such as `revised version` | Remove after completing the action, or mark the unresolved item outside the submission artifact. |
| A compact range such as `E1–E5`, `Q0–Q3`, or a new grading scale | Keep only if it names a necessary scientific construct and every category is defined at first use or in the adjacent table/legend. |
| An already defined scientific classification, named reporting framework, or ordinary section heading | Keep it. Consistency and reader comprehension, not vocabulary avoidance, control the decision. |
| Repeated unnumbered 1×1 shaded tables with the same label or structure | Three or more are a clean-copy defect: integrate the material into the section or convert a venue-required item into a formally numbered Box. |
| `Box 1`, `Box 2`, etc., or a venue-required `Key Points` block | Preserve the formal publishing element; verify the requirement and keep its numbering/function explicit. |
| `Table 1 ...` formatted as Heading 2, or obvious font-size drift inside one table | Apply a caption style and restore a deliberate, consistent table type scale. |
| Tool/draft/version language in `lastModifiedBy`, description, or the external filename | Scrub production history from the distribution copy while retaining intentional author/title metadata. |

Do not translate internal machinery into more elegant internal machinery. For
example, changing `中心判断` to `Key editorial insight` preserves the defect.
Either state the scientific conclusion under a normal content heading or keep
the judgment in the author-facing report.

Compact labels create a second risk: the writer may understand them from an
extraction sheet while the reader never sees their definitions. For each visible
code family, ask:

1. What scientific construct does the prefix encode?
2. Is each category defined where the reader first encounters it?
3. Is the same code used with the same meaning in text, tables, figures, and
   supplements?
4. Does the code reduce repeated technical wording enough to justify the reading
   cost?

Preserve established project and field classifications. For example, a defined
`C0–C4` autonomy scale should remain stable; it should not be removed simply
because the notation is compact. Conversely, a sentence saying that `E1–E5 can
serve as convenient shorthand` does not define what E1 through E5 mean and
should not enter the final paper.

Run prose-pattern and repeated-opener diagnostics on the manuscript body, not
the reference list. Journal names, DOI prefixes, and repeated bibliographic
syntax otherwise dominate the counts without describing authorial voice. The
reference list remains in scope for citation structure, DOI, invariant, metadata,
and clean-copy validation.

Do not impose a word ban. Diagnose the referent and function in context.

## When common abstract nouns are legitimate

| Term | Legitimate use | Likely scaffolding leakage |
|---|---|---|
| `evidence` / `证据` | distinguishing clinical, in vivo, mechanistic, or prospective support | a generic subject or glue word when the underlying observation can be named |
| `dataset` / `数据集` | a defined collection with samples, provenance, variables, and splits | a loose substitute for measurements, images, records, formulations, or study results |
| `framework` / `框架` | a named reporting standard, mathematical formulation, software system, or genuinely new taxonomy | any ordinary organization, sequence, comparison, or point of view |
| `pipeline` / `workflow` / `流程` | an implemented computational or experimental sequence with identifiable stages | decorative movement between topics or a synonym for “approach” |
| `closed loop` / `闭环` | results from one experiment change the model's next experimental choice | general iteration, automation, or feedback with no decision update |
| `benchmark` / `基准` | a specified task, split, metric, comparator, and evaluation protocol | a wish list for better data or a generic quality standard |
| `boundary` / `边界` | a domain of applicability or tested physical/biological condition | repeated shorthand for every limitation or uncertainty |

Named technical terms should remain stable. The repair is to remove vague uses,
not to disguise correct terminology with synonyms.

## Write the synthesis at the object level

Weak editorial summary:

> These studies build an evidence chain that bridges the in vitro--in vivo gap.

Object-level synthesis:

> In vitro delivery rankings changed substantially in animals, so cell-based
> screening can eliminate poor formulations but cannot rank organ delivery on
> its own.

Weak editorial summary:

> This framework integrates multimodal datasets across the discovery pipeline.

Object-level synthesis:

> The model combines lipid structure, formulation ratios, synthesis conditions,
> microscopy, and organ-level delivery measurements; candidates without animal
> data remain outside the transfer analysis.

Weak Chinese summary:

> 这些研究构建了从数据集到体内证据的完整链路。

Object-level Chinese synthesis:

> 体外转染结果只能排除明显无效的配方；器官分布和细胞趋向性仍需在动物中
> 分别测定，二者不能由同一个体外排序替代。

The stronger versions state what was compared, what changed, and what remains
untested. They do not merely rename the act of reviewing.

## Paragraph patterns used by strong reviews

Choose the pattern that matches the reasoning; do not rotate through these as
templates.

- **Object -> constraint -> consequence:** name the material or task, explain the
  limiting property, then state what that requires of the method.
- **Studies -> methodological difference -> interpretation:** group studies that
  answer the same question and explain why their different designs change the
  conclusion.
- **Result -> failed transfer -> narrower claim:** state the observed result,
  identify where it failed to generalize, and reduce the claim accordingly.
- **Capability -> required control:** explain what a method enables and name the
  baseline, split, intervention, or prospective test needed to trust it.
- **Named exception -> revised rule:** use an outlying study to refine a general
  statement instead of adding another catalogue entry.

Sentence variety should follow these reasoning moves. It should not be produced
by random synonym replacement, forced sentence-length alternation, or deletion
of necessary technical repetition.

## Review-specific leakage checks

Flag for human review, rather than deleting mechanically:

- repeated `we propose`, `we present`, `this Review`, `本文提出`, or `本文构建`;
- headings built from `framework`, `landscape`, `paradigm`, `evidence`, `图谱`,
  `体系`, `赋能`, or `闭环` when a concrete scientific question would be clearer;
- paragraphs in which most sentence subjects are abstract nouns;
- successive sentences that end with a generic boundary, implication, or future
  need without specifying the experiment or comparison;
- `dataset` where the sample unit and provenance are never stated;
- `evidence chain` or `证据链` used to conceal that one inferential step has not
  actually been tested.

The final test is not whether a target word disappeared. It is whether a domain
researcher can identify the scientific object, the comparison, the observed or
reported result, and the remaining limit in each consequential paragraph.
