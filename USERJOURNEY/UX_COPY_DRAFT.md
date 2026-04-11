# UX_COPY_DRAFT.md

Purpose: Draft screen copy and product language for signup, verification, onboarding, consent, and first-run activation.
Owner: Solo operator
Last updated: 2026-04-01
Depends on: PRODUCT_SPEC.md, USER_FLOWS.md, LEGAL_AND_CONSENT.md
Authority: Working UX copy draft for the USERJOURNEY package

---

## Guidance

This is product copy direction, not final brand copy. It is designed to reduce ambiguity, set expectations, and improve trust during first-run.

This draft applies to the planned end-user onboarding route family. It does not describe or validate the local operator dashboard in this template repository.

## Screen 1: Auth Entry

### Primary Heading

Build, tailor, and improve your resume in one workspace.

### Supporting Copy

Upload an existing resume or start from scratch. Save versions, tailor to job descriptions, and export polished results when you're ready.

### Primary Actions

- Sign in
- Create account

### Trust Copy

Your account lets you save resumes, versions, and job-specific work in one place.

## Screen 2: Create Account

### Heading

Create your account

### Supporting Copy

Start with your email and password. You can import a resume or build one after verification.

### Field Labels

- Email address
- Password
- Confirm password

### Required Consent Copy

I agree to the Terms of Service and Privacy Policy.

### Optional Consent Copy

Send me product updates and release notes.

### Submission CTA

Create account

### Footer Link

Already have an account? Sign in.

## Screen 3: Verification Pending

### Heading

Check your email to verify your account

### Supporting Copy

We sent a verification link to your email address. Open it to continue setting up your resume workspace.

### Actions

- Resend email
- Change email
- Back to sign in

### Secondary Note

If you do not see the email in a few minutes, check spam or resend the link.

## Screen 4: Verification Recovery

### Heading

That verification link did not work

### Supporting Copy

The link may be expired, invalid, or already used. You can request a new verification email and continue setup.

### Actions

- Resend verification email
- Back to sign in

## Screen 5: Welcome / Onboarding Intro

### Heading

Let's get your first resume workspace ready

### Supporting Copy

This only takes a couple of minutes. You can upload an existing resume, build one from scratch, or skip guided setup for now.

### Primary Actions

- Import my resume
- Start from scratch
- Skip setup for now

### Expectation Copy

You will have a saved profile and a usable starting point before you enter the full workspace.

### Skip Copy

If you want, you can skip guided setup and enter the workspace now. You can complete setup later, but some features will still ask for required information before you use them.

## Screen 6: AI And Data Notice

### Heading

Before you continue

### Body Copy

Your resume and job description content may be stored in your account so you can keep working on it later. Some features may also process that content with AI-powered services to analyze, improve, or tailor your documents.

AI suggestions can be incomplete, inaccurate, or misleading, so you should review all output before using it.

### Actions

- Continue
- Go back

### Optional Fine Print

You can review the Privacy Policy and Terms of Service at any time.

## Screen 7: Import Resume

### Heading

Import your existing resume

### Supporting Copy

Upload a PDF, DOCX, or TXT file. We will extract the content and let you review it before saving your profile.

### Primary CTA

Upload resume

### Secondary Note

Parsing is a starting point. You will be able to correct anything that looks wrong before continuing.

### File Validation Error

We could not accept that file. Make sure it is a PDF, DOCX, or TXT file and try again.

### Parse Failure

We were not able to read the content in that file. It may be password-protected, scanned as an image, or in a format we do not yet support. Try exporting as a plain DOCX or PDF, or use the start-from-scratch option instead.

### Heading

Review what we found

### Supporting Copy

We extracted the sections below from your resume. Check them now so your saved profile starts from the right information.

### Primary CTA

Save and continue

### Secondary CTA

Edit extracted content

### Helper Copy

Small fixes here will improve tailoring and rewrite suggestions later.

## Screen 9: Start From Scratch

### Heading

Start your resume from scratch

### Supporting Copy

Tell us the basics and we will create your first working draft and workspace.

### Suggested Inputs

- Full name
- Email
- Current or target role
- Experience highlights
- Key skills

### CTA

Create my profile

## Screen 10: Choose Your First Goal

### Heading

What do you want to do first?

### Options

- Improve my current resume
- Tailor it to a job description
- Build a fresh version

### Supporting Copy

We will use this to shape your first workspace and next-step recommendations.

## Screen 11: Activated Workspace Empty-State Copy

### If Imported Resume Exists

Your resume is ready to work on. Start improving sections, tailor to a job description, or export when you are ready.

### If Starter Profile Exists

Your first draft is ready. Add experience details, strengthen bullets, or tailor the resume to a role.

### If Tailoring Was Selected

Paste a job description to start tailoring your resume to a real opportunity.

## Screen 12: Minimal Workspace (Skipped Setup)

### Persistent Setup Banner

Setup is not complete. Some features will ask for required steps before you can use them.

### Banner CTA

Complete setup

### Workspace Entry Heading

You are in your workspace

### Supporting Copy

You skipped guided setup, so no resume has been created yet. You can explore the workspace now, but upload and AI features will walk you through required steps the first time you use them.

### Empty-State Copy

No resume yet. Complete setup to create your first profile and unlock full workspace features.

### Recovery CTA

Start setup now

### Inline Reminder (visible until activation)

Your workspace is ready, but you have not yet reached your first usable result. Complete setup when you are ready.

## Tone Rules

1. Use direct language.
2. Avoid generic AI hype.
3. Avoid legalese in product surfaces.
4. Tell the user what happens next.
5. Acknowledge that AI output needs review.
