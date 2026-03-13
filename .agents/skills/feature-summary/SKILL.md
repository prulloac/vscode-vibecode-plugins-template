---
name: feature-summary
description: Create comprehensive feature documentation summaries that describe current and future capabilities. Use after feature-breakdown to document what a feature does, its business value, technical implementation, and roadmap. Ideal for creating user-facing documentation and feature catalogs in `docs/features/<feature-name>/` format.
---

# Feature Summary Skill

**Answers the question: How do we DOCUMENT and COMMUNICATE a feature to stakeholders, users, and developers?**

This skill focuses on **feature documentation and communication**, transforming detailed breakdowns into accessible, comprehensive summaries that serve multiple audiences.

## When to Use

Use this skill when you have a **completed feature** (or a detailed feature breakdown) and need to:

- Create comprehensive user-facing documentation
- Build a feature catalog or knowledge base
- Document business features for stakeholder communication
- Explain technical implementation to developers
- Create feature roadmaps and status tracking
- Document current and future capabilities
- Classify features by type (core, customization, performance, accessibility, UX)

**Key indicator**: You're asking "How do we document and communicate this feature?" or "What should users know about this capability?"

**Works best with**: This skill complements `feature-breakdown` (provides the detailed task list) and `feature-planning` (provides the execution sequence)

## When NOT to Use

- You only have a feature idea/spec without breakdown details → Use `feature-breakdown` first
- You need to determine task execution order → Use `feature-planning` instead
- You need to track real-time implementation progress → Use `execution-tracking` instead

## Prerequisites

Recommended (but not strictly required):

1. **Feature breakdown** (`docs/features/[feature-name]/breakdown.md`)

   - Provides detailed task list and component architecture
   - Helps identify all feature aspects to document

1. **Feature implementation** (completed or well-understood)

   - Access to working code or specifications
   - Understanding of current status

1. **Audience understanding**

   - Who will read this documentation?
   - What do they need to know?

## Inputs

- **Feature specification or implemented feature** (required)
- **Feature breakdown document** (recommended): `docs/features/[feature-name]/breakdown.md`
- **Source code access** (optional but helpful): For accurate implementation details
- **Usage examples** (optional): For user documentation

## Directory Structure

All feature-summary output must follow this structure:

```
docs/features/[feature-name]/
├── breakdown.md              (created by feature-breakdown skill)
├── summary.md                (created by this skill - PRIMARY OUTPUT)
├── configuration.md          (optional - created by this skill)
├── reference.md              (optional - created by this skill)
└── implementation-progress.md (created by execution-tracking skill during implementation)
```

## Outputs

**MANDATORY FILE ORGANIZATION**: All feature documentation must be in `docs/features/<feature-name>/` subdirectory.

When this skill completes, it creates:

1. **Primary Output: Feature Summary** (`docs/features/[feature-name]/summary.md`)

   - Comprehensive feature documentation
   - 150-250 lines covering all major aspects
   - Serves multiple audiences (users, developers, stakeholders)
   - Includes feature type classification
   - **Example**: `docs/features/git-blame-overlay/summary.md`

1. **Optional: Configuration Reference** (`docs/features/[feature-name]/configuration.md`)

   - Detailed configuration options and examples
   - For features with significant customization

1. **Optional: Reference Guide** (`docs/features/[feature-name]/reference.md`)

   - Technical implementation details for developers
   - Architecture decisions and patterns

1. **Supporting Structure**:

   - `docs/features/[feature-name]/breakdown.md` - Implementation tasks (created by feature-breakdown skill)
   - `docs/features/[feature-name]/implementation-progress.md` - Tracking file (created by execution-tracking skill)

## Workflow Overview

The feature summary process transforms a feature concept into comprehensive documentation:

```
Feature Input (Breakdown or Implementation)
    ↓
Analyze Feature Aspects
    ↓
Identify Audiences & Use Cases
    ↓
Classify Feature Type
    ↓
Create Executive Summary
    ↓
Document Configuration & Options
    ↓
Explain Technical Implementation
    ↓
Define Status & Version Info
    ↓
Identify Limitations & Future Enhancements
    ↓
Write Output Files
    ↓
Comprehensive Feature Documentation
```

## Core Workflow

### Phase 1: Analyze Feature Scope

**Input**: Feature specification, breakdown, or implementation

1. **Identify feature aspects**:

   - What does it do? (Core functionality)
   - Why is it valuable? (Business value)
   - How do users interact with it? (User experience)
   - What are the key capabilities? (Feature list)
   - What are the limitations? (Edge cases and constraints)

1. **Extract technical details**:

   - How is it implemented? (Architecture, components)
   - What are the technical requirements? (Dependencies, prerequisites)
   - Where is the code located? (Source file references)
   - What patterns or technologies are used?

1. **Understand current state**:

   - Version number and release status
   - When was it introduced?
   - What improvements or fixes have been made?
   - Is it production-ready?

### Phase 2: Classify Feature Type

Assign the feature to one or more categories:

| Category                   | Description                                              | Examples                                       |
| -------------------------- | -------------------------------------------------------- | ---------------------------------------------- |
| **Core Functionality**     | Essential feature defining the product's primary purpose | Git blame overlay, authentication system       |
| **Customization**          | Allows users to personalize behavior and appearance      | Output patterns, color customization           |
| **User Experience**        | Improves usability, visual integration, and workflow     | Theme adaptation, command palette              |
| **Accessibility**          | Supports users with different abilities and needs        | Color options, keyboard shortcuts, ARIA labels |
| **Performance**            | Optimizes speed and resource usage                       | Caching, lazy loading, pagination              |
| **Extended Functionality** | Non-essential features that enhance core capability      | Advanced filtering, export options             |
| **Developer Experience**   | Improves developer productivity and experience           | Debugging tools, API documentation             |

## Output Format

Feature summaries include these key sections (in order):

1. **Feature Header** - Name, overview, status, version, feature type
1. **Business Value** - Why it matters, specific benefits
1. **What It Does** - Core functionality with user experience and examples
1. **Key Features** - Capabilities and extended functionality
1. **Configuration** (if applicable) - Options and examples
1. **Technical Implementation** - Code references and architecture
1. **User Interactions** - Workflows and commands
1. **Status and Roadmap** - Current status, limitations, future enhancements
1. **Related Features** - Cross-references to related features

**For a complete template with examples and detailed guidelines**, see:

- [`assets/documentation-template.md`](assets/documentation-template.md) - Blank template for creating new features
- [`examples/example-feature-summary-core.md`](examples/example-feature-summary-core.md) - Core functionality example
- [`examples/example-feature-summary-customization.md`](examples/example-feature-summary-customization.md) - Customization example
- [`examples/example-feature-summary-performance.md`](examples/example-feature-summary-performance.md) - Performance example

## Feature Type Classification

Every feature should be classified with a primary type and optional secondary types. This helps users understand:

- **What is this feature?** (Its purpose)
- **Is it essential?** (Core vs. optional)
- **How does it relate to other features?** (Ecosystem awareness)

### Quick Reference

| Type                       | Icon | Purpose                            | Example             |
| -------------------------- | ---- | ---------------------------------- | ------------------- |
| **Core Functionality**     | ⭐   | Essential, defines product purpose | Git blame overlay   |
| **Customization**          | 🎨   | Personalization & preferences      | Output patterns     |
| **User Experience**        | 👥   | Usability & visual integration     | Theme-aware styling |
| **Accessibility**          | ♿   | Support for diverse users          | Color options       |
| **Performance**            | 🚀   | Speed & resource optimization      | Caching system      |
| **Extended Functionality** | ➕   | Optional enhancements              | Export options      |
| **Developer Experience**   | 🛠️   | Developer productivity             | API docs            |

**For detailed guidance on each type**, see [`references/feature-type-reference.md`](references/feature-type-reference.md)

## Guidelines

### Writing for Multiple Audiences

**For Users**:

- Use clear, non-technical language
- Explain benefits and use cases
- Provide concrete examples
- Include configuration examples

**For Developers**:

- Include code references and file paths
- Explain architecture and design decisions
- Document patterns and conventions
- Link to technical documentation

**For Stakeholders**:

- Lead with business value
- Emphasize impact and ROI
- Focus on status and roadmap
- Quantify benefits where possible

### Feature Classification

When assigning feature types:

1. **Identify primary category**: What is this feature's main purpose?
1. **Note secondary categories**: Can it serve multiple purposes?
1. **Explain classification**: Why does this categorization make sense?
1. **Consider user perception**: How do users think about this feature?

### Technical Accuracy

- Reference actual source code paths
- Include line numbers for specific implementations
- Verify all code examples work correctly
- Document technical constraints accurately

### Keeping Documentation Current

- Update status section when feature versions change
- Add to limitations if new constraints are discovered
- Move items from "Future Enhancements" when implemented
- Update configuration examples if options change

## Common Pitfalls to Avoid

❌ **Too technical for users**: Remember non-technical readers; explain technical concepts
❌ **Too vague for developers**: Provide specific code references and implementation details
❌ **Incomplete feature classification**: Always explain why a feature fits its category
❌ **Missing examples**: Concrete examples are crucial for understanding
❌ **Outdated information**: Keep status and version info current
❌ **Poor cross-linking**: Reference related features; help readers understand relationships
❌ **Missing technical details**: Developers need code references and architecture info

## Integration with Other Skills

The feature-summary skill works as part of a larger feature documentation ecosystem. For detailed integration workflows and examples:

- **Overview of the skill ecosystem**: [`references/ecosystem-diagram.md`](references/ecosystem-diagram.md)
- **Practical integration workflows**: [`references/workflow-integration-guide.md`](references/workflow-integration-guide.md)
- **Quick navigation**: [`references/integration-guide.md`](references/integration-guide.md)

### Recommended Skill Sequence

1. **feature-breakdown** (1-2 hrs) - Decompose feature into tasks and acceptance criteria
1. **feature-summary** (1-2 hrs) - Create user-facing documentation
1. **feature-planning** (1-2 hrs) - Sequence tasks for execution
1. **execution-tracking** (ongoing) - Monitor implementation progress

### Key Concepts

**feature-breakdown creates** (`docs/features/[name]/breakdown.md`):

- Internal task list
- Component architecture
- Acceptance criteria
- Validation plan

**feature-summary creates** (`docs/features/[name]/summary.md`):

- User-facing documentation
- Business value explanation
- Configuration examples
- Roadmap and future enhancements

## Quality Checklist

Before finalizing feature documentation:

- [ ] Feature type classification is clear and explained
- [ ] Business value section explains "why" not just "what"
- [ ] Examples show real-world usage
- [ ] Technical details are accurate with code references
- [ ] Configuration options are clearly documented
- [ ] Status and version info are current
- [ ] Known limitations are honestly documented
- [ ] Future enhancements are realistic and categorized
- [ ] Cross-references to related features are accurate
- [ ] Documentation is accessible to intended audiences
- [ ] Language is clear and concise
- [ ] All file paths and code references are accurate

## Example Output

For a real example of how feature documentation should look, see the example feature summaries:

- Reference: `examples/example-feature-summary-core.md` (Core functionality example)
- Reference: `examples/example-feature-summary-customization.md` (Customization example)
- Reference: `examples/example-feature-summary-performance.md` (Performance feature example)

## See Also

- `feature-breakdown` - Decompose features into tasks
- `feature-planning` - Sequence tasks for execution
- `execution-tracking` - Monitor feature implementation progress
- `readme-updater` - Keep project README in sync with features
