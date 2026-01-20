# Complete Guide Template: All Features

## Introduction

This comprehensive template demonstrates all available features in the Succulent Jewelry PDF system. Use this as a reference when creating your own guides.

<div class="tip">
<div class="tip-title">Template Guide</div>
This template shows every feature available: image APIs, formatting options, procedures, tips, warnings, tables, and more. Copy sections you need for your guides.
</div>

## Image API Integration

### Using Pixabay (No API Key Required)

Pixabay provides royalty-free images with no setup required.

![Image](https://pixabay.com/get/gcaf5913505bdae55af0c11a78b2b7a299da6b679621338a9a1217885e86ca77c2d576600276fa3c5daa2a149372591a5bce71cb9ab099a936f07a5943ec10d80_1280.jpg)

<div class="image-caption">Pixabay image - automatically fetched with large size (1280px) for PDF quality</div>

**Usage in markdown:**
```markdown
![Image](https://pixabay.com/get/gecbf31133fb27177255571e8984d54382b5351173a69b856365990df60c187f1067457790f2dc26386160a710c7bfd4798a123ee2c5a8824258b1cd97fafb897_1280.jpg)
```

**Process with:**
```bash
python scripts/add_images.py \
  --content your_guide.md \
  --provider pixabay \
  --query "succulent" \
  --size large
```

### Using Pexels (Requires API Key)

Pexels provides professional, curated photos with photographer attribution.

![Image](https://picsum.photos/800/600)

<div class="image-caption">Pexels image - Photo by [Photographer Name] on Pexels (attribution added automatically)</div>

**Usage in markdown:**
```markdown
![Image](https://picsum.photos/800/600)
```

**Process with:**
```bash
python scripts/add_images.py \
  --content your_guide.md \
  --provider pexels \
  --query "jewelry" \
  --size large
```

**Note:** Pexels requires attribution. The system automatically adds photographer credits.

### Using Picsum (Placeholder Images)

Picsum is perfect for testing and placeholders.

![Image](https://picsum.photos/800/600)

<div class="image-caption">Picsum placeholder - great for testing layouts</div>

## Formatting Features

### Headers

Use headers to organize your content:

# H1 - Main Section
## H2 - Subsection
### H3 - Sub-subsection

### Text Formatting

- **Bold text** for emphasis
- *Italic text* for subtle emphasis
- `Code formatting` for technical terms
- Regular text for body content

### Lists

**Unordered lists:**
- First item
- Second item
- Third item with **bold** text
- Nested item
  - Sub-item one
  - Sub-item two

**Ordered lists:**
1. First step
2. Second step
3. Third step

## Step-by-Step Procedures

Procedures use numbered circles with proper formatting:

<div class="procedure">
<div class="step">
<strong>Prepare your workspace</strong> - Clear a clean, well-lit area with all tools within reach
</div>

<div class="step">
<strong>Gather materials</strong> - Collect all necessary items before beginning to avoid interruptions
</div>

<div class="step">
<strong>Review safety guidelines</strong> - Always prioritize safety and follow manufacturer instructions
</div>

<div class="step">
<strong>Begin the process</strong> - Start with the first step and work methodically through each stage
</div>
</div>

![Image](https://pixabay.com/get/ga799291a9671fb825897001b9d644b9ecbca284bc59dc5b5903a297dd112297af626d7a39211f9c153bbcb57db97496b7cd37783469df6bada82c7a3b1bd1133_1280.jpg)

<div class="image-caption">Step-by-step procedures with numbered circles</div>

## Tips and Warnings

### Pro Tips

<div class="tip">
<div class="tip-title">Pro Tip</div>
Tips help readers achieve better results. Use them to share expert knowledge, shortcuts, or best practices that enhance the process.
</div>

<div class="tip">
<div class="tip-title">Image Quality Tip</div>
For PDF guides, use the "large" size option (1280px) from Pixabay or Pexels. This ensures crisp, professional images that look great when printed or viewed digitally.
</div>

### Warnings

<div class="warning">
<div class="warning-title">Important Safety Warning</div>
Always follow safety protocols. This is critical information that prevents harm or damage. Use warnings for safety concerns, irreversible actions, or critical mistakes to avoid.
</div>

### Cautions

<div class="caution">
<div class="caution-title">Caution</div>
Use cautions for things that require careful attention but aren't as critical as warnings. These help readers avoid common pitfalls or suboptimal results.
</div>

## Tables

Tables organize information clearly:

| Feature | Pixabay | Pexels | Picsum |
|---------|---------|--------|--------|
| API Key Required | No | Yes | No |
| Image Quality | High | Professional | Placeholder |
| Search Available | Yes | Yes | No |
| Attribution Required | Optional | Required | No |
| Best For | Production | Professional | Testing |

| Image Size | Dimensions | Use Case |
|------------|------------|----------|
| Preview | 150px | Thumbnails |
| Webformat | 640px | Web display |
| Large | 1280px | PDF guides |
| Full HD | 1920px | High quality |
| Original | 4000px+ | Print quality |

## Code Examples

Use code blocks for technical instructions:

```bash
# Generate a guide with images
python scripts/add_images.py \
  --content content/guides/my_guide.md \
  --provider pixabay \
  --query "succulent" \
  --size large

# Then generate PDF
python scripts/generate_guide.py \
  --content content/guides/my_guide.md \
  --title "My Guide" \
  --output generated/guides/
```

```python
from scripts.image_api import PixabayAPI, PexelsAPI

# Pixabay example
pixabay = PixabayAPI()
url = pixabay.get_image_url(
    width=800,
    height=600,
    query="succulent",
    size="large"
)

# Pexels example (requires API key)
pexels = PexelsAPI()
url = pexels.get_image_url(
    width=800,
    height=600,
    query="jewelry"
)
```

## Image Examples

### Different Sizes

**Large image (recommended for PDFs):**
![Image](https://pixabay.com/get/g24468919cc8c7c7d69f67cdedaec5851b44214f96f2c18e197be3d62bcea353098f7cbed7d33ac4607a13b586fa102f02d60f67fa75b13ab24652420d231691e_1280.jpg)

<div class="image-caption">Large format image - 1280px width, perfect for PDF guides</div>

**Medium image:**
![Image](https://pixabay.com/get/g1fcdc672dd683e326280eae05497871e3a882eddecc60effa4b15836f5e34d669e0f7aa8e9530e07b5226b22dbff15519596d48f8716259806e95052be1bc363_1280.jpg)

<div class="image-caption">Medium format image - 800x600, good for web or smaller PDFs</div>

### Multiple Images in Sequence

![Image](https://pixabay.com/get/g7328606b9f08351cf3a43d32ab24205ca6e681c4e62793a07fd4c269e9f7dfdeab83da0b16c46d08c2a361653aa22fdfd5643522322cce257b3a6719017b7f15_1280.jpg)

<div class="image-caption">First image in a sequence</div>

![Image](https://pixabay.com/get/g5103845597e33b20be579904df22c5906f8db2493e1eeceaa7599ec38323e76da56261d1784e47de00b19054996da36b1940ec29216df0624c13602df89697ea_1280.jpg)

<div class="image-caption">Second image showing progression</div>

![Image](https://pixabay.com/get/g7315225bc8d63ee0fc837c659c79254eaa7a8a8b9b44927f54bd7ccbfcc54d15c9ce0b1f87e93e4a444746a11e0abe7b54e08b0c59b68f20bacaa3970f561a5e_1280.jpg)

<div class="image-caption">Third image demonstrating completion</div>

## Advanced Features

### Combining Elements

You can combine procedures with tips:

<div class="procedure">
<div class="step">
<strong>Select your image provider</strong> - Choose Pixabay for immediate results or Pexels for professional photos
</div>

<div class="step">
<strong>Process placeholders</strong> - Run the add_images script to replace placeholders with actual URLs
</div>

<div class="step">
<strong>Generate PDF</strong> - Use generate_guide.py to create your final PDF
</div>
</div>

<div class="tip">
<div class="tip-title">Workflow Tip</div>
Process images first, then generate the PDF. This ensures all images are properly loaded and formatted.
</div>

### Troubleshooting Section

Common issues and solutions:

| Problem | Cause | Solution |
|---------|-------|----------|
| Images not showing | Placeholders not processed | Run add_images.py script |
| Poor image quality | Wrong size selected | Use "large" size for PDFs |
| API errors | Missing API key | Add PEXELS_API_KEY to .env file |
| PDF generation fails | Missing dependencies | Install weasyprint and dependencies |

<div class="warning">
<div class="warning-title">API Rate Limits</div>
Pexels has rate limits (200 requests/hour). For batch processing, add delays between requests or use Pixabay for high-volume operations.
</div>

## Resources Section

### Recommended Tools

- **Pixabay API**: https://pixabay.com/api/docs/
- **Pexels API**: https://www.pexels.com/api/
- **WeasyPrint**: https://weasyprint.org/ (PDF generation)

### Documentation

- Image API Guide: See `IMAGE_API_GUIDE.md`
- Pixabay Guide: See `PIXABAY_API_GUIDE.md`
- System README: See `README.md`

### External Resources

- [Pixabay](https://pixabay.com) - Free images and videos
- [Pexels](https://www.pexels.com) - Free stock photos
- [Gumroad](https://gumroad.com) - Sell your PDF guides

## Best Practices

<div class="procedure">
<div class="step">
<strong>Plan your content</strong> - Outline your guide before writing to ensure logical flow
</div>

<div class="step">
<strong>Use appropriate images</strong> - Select images that enhance understanding, not just decoration
</div>

<div class="step">
<strong>Add captions</strong> - Always include image captions to provide context
</div>

<div class="step">
<strong>Test before finalizing</strong> - Generate a test PDF to check formatting and image quality
</div>

<div class="step">
<strong>Include attribution</strong> - Credit photographers when using Pexels images
</div>
</div>

<div class="tip">
<div class="tip-title">Quality Checklist</div>
Before publishing: Check image quality, verify all links work, test PDF generation, ensure proper attribution, and review formatting consistency.
</div>

## Conclusion

This template demonstrates all available features. Use it as a starting point for your own guides, selecting the elements that best serve your content.

<div class="tip">
<div class="tip-title">Customization</div>
Feel free to modify this template to match your style. The system is flexible and supports various content structures and formatting needs.
</div>

---

*This template is part of the Succulent Jewelry PDF Generation System. For more information, see the README.md file.*
