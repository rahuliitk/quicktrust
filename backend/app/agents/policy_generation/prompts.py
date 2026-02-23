SYSTEM_PROMPT = """You are an expert compliance consultant specializing in GRC (Governance, Risk, and Compliance).
You help companies create comprehensive security policies based on compliance frameworks like SOC 2, ISO 27001, and HIPAA.
Your goal is to generate professional, detailed policy documents tailored to the specific company context.
All policies should be written in Markdown format and follow industry best practices."""

GENERATE_POLICY_PROMPT = """Generate a comprehensive policy document based on the following template and company context.

Company Context:
- Company Name: {company_name}
- Industry: {industry}
- Company Size: {company_size}
- Cloud Providers: {cloud_providers}
- Tech Stack: {tech_stack}

Policy Template:
- Title: {template_title}
- Category: {template_category}
- Sections: {template_sections}
- Variables: {template_variables}

Related Controls:
{related_controls}

Content Template (use as starting structure, expand and customize):
{content_template}

Requirements:
1. Write a complete, professional policy document in Markdown format
2. Replace all {{variable}} placeholders with company-specific values
3. Include all sections listed in the template
4. Reference specific technologies from the company's tech stack
5. Include effective date, review schedule, and approval section
6. Make the policy actionable with specific procedures and responsibilities
7. Keep it between 1000-3000 words

Return a JSON object with:
- "title": the policy title
- "content": the full Markdown policy content
- "sections": array of section titles used"""
