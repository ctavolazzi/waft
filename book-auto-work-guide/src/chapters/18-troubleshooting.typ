= Troubleshooting

This chapter covers common issues and solutions.

== No Work Efforts Found

*[Problem]*: `❌ No work efforts found.`

*[Solution]*:
- Check that `_work_efforts/` directory exists
- Verify work effort directories follow `WE-YYMMDD-xxxx` format
- Ensure work efforts are in the correct location

== No Actionable Work Efforts

*[Problem]*: `❌ No actionable work efforts found (all completed).`

*[Solution]*:
- Create new work efforts
- Reopen paused work efforts
- Change status from `completed` to `active` or `paused`

== Action Not Available

*[Problem]*: `❌ No actions available for this work effort.`

*[Solution]*:
- Check work effort has index file
- Verify work effort structure
- Ensure work effort is not empty

== Safety Gate Halt

*[Problem]*: `❌ Execution halted by safety gate`

*[Solution]*:
- Review Empirica gate reason
- Check Judge verdict
- Manually approve if safe
- Revise approach if needed

== Integration Unavailable

*[Problem]*: `⚠️  Empirica: Not initialized`

*[Solution]*:
- Initialize Empirica (optional)
- System continues without it
- Check initialization logs

== Next Steps

Now let's explore customization options.
