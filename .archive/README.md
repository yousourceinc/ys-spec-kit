# Archive

This directory contains historical and one-off documentation files from earlier phases of development. These files are kept for reference but are no longer actively maintained.

## Contents

### Release & Status Documents

**v0.4.0 Release Artifacts** (Archived 2025-10-22)
- `v0.4.0_RELEASE_STATUS.md` - Release status and tracking document
- `RELEASE_NOTES_v0.4.0.md` - See current releases in `/project-meta/releases/`
- `MERGE_COMPLETE_v0.4.0.md` - Merge completion tracking

### Implementation Checklists

**OAuth Implementation** (Completed 2025-10-20)
- `OAUTH_IMPLEMENTATION_CHECKLIST.md` - Original checklist (feature complete)
- `OAUTH_IMPLEMENTATION_COMPLETE.md` - Completion summary

**Guides Implementation** (Completed 2025-10-21)
- `GUIDES_IMPLEMENTATION_COMPLETE.md` - Guides phase completion

### Documentation Templates

**Pull Request Template** (Superseded by standard)
- `PULL_REQUEST_TEMPLATE_v0.4.0.md` - Version 0.4.0 specific template
  - Note: Project now uses standard PR template

## Why These Files Are Here

When documentation was reorganized on 2025-10-22:

1. **One-off tracking documents** were archived instead of deleted
   - Example: `OAUTH_IMPLEMENTATION_CHECKLIST.md` (feature now complete)
   - These tracked specific milestones that have already passed

2. **Version-specific artifacts** were moved to project-meta
   - Release notes → `/project-meta/releases/`
   - Status documents → `/project-meta/status/`
   - Completion summaries → `/project-meta/completion-logs/`

3. **Obsolete templates** were archived
   - Pull request templates are now standardized
   - Version-specific templates no longer needed

## Accessing Historical Information

### Looking for Release Information?
→ See `/project-meta/releases/README.md`

### Looking for Completion Logs?
→ See `/project-meta/completion-logs/README.md`

### Looking for Project Status?
→ See `/project-meta/status/README.md`

### Looking for Current Guides?
→ See `/docs/guides/`

## Using Archive Files

Files in this directory are **read-only reference**. If you need to:

1. **Reference old implementation details**: Check the relevant file here
2. **Update information**: Create new files in appropriate locations:
   - Guides: `/docs/guides/`
   - Status: `/project-meta/status/`
   - Releases: `/project-meta/releases/`
   - Completion: `/project-meta/completion-logs/`

## Git History

All archived files remain in the git history. To view the history of any file:

```bash
git log --follow .archive/FILENAME
git show COMMIT_HASH:.archive/FILENAME
```

## When to Delete Archive Files

Archive files are candidates for deletion when:
- [ ] Feature implementation is 2+ major versions old
- [ ] No active references to the file remain
- [ ] Team confirms file is no longer needed for reference
- [ ] Git history has been preserved

For example: `OAUTH_IMPLEMENTATION_CHECKLIST.md` (2025-10-20) could be deleted in v0.5.0 (2026-Q2).

## Maintenance

This archive is maintained as part of the documentation reorganization effort. New one-off documents should NOT be added here without team discussion.

Suggested practice:
1. Create files in appropriate permanent locations
2. Keep archive for historical reference only
3. Review annually for cleanup candidates

---

**Archive Created**: 2025-10-22  
**Total Files**: 7  
**Total Size**: ~150 KB  
**Last Reviewed**: 2025-10-22

**Files in Archive**:
1. OAUTH_IMPLEMENTATION_CHECKLIST.md
2. OAUTH_IMPLEMENTATION_COMPLETE.md
3. v0.4.0_RELEASE_STATUS.md
4. MERGE_COMPLETE_v0.4.0.md
5. GUIDES_IMPLEMENTATION_COMPLETE.md
6. PULL_REQUEST_TEMPLATE_v0.4.0.md
7. (and this README)
