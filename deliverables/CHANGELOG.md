# Changelog

## Report generator enhancements

### Completed and verified

- Added centralized report-style constants.
- Added reusable longtable continuation-header handling.
- Split vehicle and footpath live-load presentation.
- Made footpath reporting follow the selected bridge geometry.
- Corrected metre-to-millimetre display for girder section dimensions.
- Added UR chart generation with pass/fail coloring and UR = 1.0 threshold.
- Added material quantity chart generation.
- Replaced generic figure placeholder wording.

### Added but awaiting fresh-PDF verification

- Connected the existing headless CAD export routine to report figure bytes.

### Still open

- Prevent Table 5.4 member groups from splitting across pages.
- Calculate and display End Diaphragm quantities when model data supports it.
- Complete wind and seismic report-field mapping.
- Correct final page-count reference.
- Validate and correct the IRC 5 reference year.
- Generate final `Report_After.pdf` and submission documentation package.

