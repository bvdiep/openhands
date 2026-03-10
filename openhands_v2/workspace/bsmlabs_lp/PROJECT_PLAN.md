# BSMLabs Landing Page - WordPress Theme Development Plan

## Project Overview
Phát triển WordPress theme tùy chỉnh dựa trên phân tích Base.vn để tạo landing page chuyên nghiệp cho BSMLabs với focus vào enterprise solutions.

---

## Theme Structure

### Core PHP Files
```
bsmlabslp/
├── style.css                    # Theme header & main styles
├── index.php                    # Fallback template
├── front-page.php              # Homepage template
├── header.php                   # Site header
├── footer.php                   # Site footer
├── functions.php                # Theme functions & setup
├── screenshot.png               # Theme preview
├── 404.php                      # Error page
├── single.php                   # Single post template
├── page.php                     # Single page template
├── archive.php                  # Archive template
├── search.php                   # Search results
└── template-parts/
    ├── content-hero.php         # Hero section
    ├── content-platforms.php    # Platform showcase
    ├── content-industries.php   # Industry tabs
    ├── content-testimonials.php # Customer stories
    ├── content-cta.php          # Call-to-action
    ├── navigation/
    │   └── mobile-menu.php      # Mobile navigation (Max Mega Menu handles desktop)
    └── blocks/
        ├── hero-block.php       # Hero section block
        ├── platform-block.php   # Platform showcase block
        ├── industry-block.php   # Industry tabs block
        ├── testimonial-block.php # Testimonials block
        ├── cta-block.php        # CTA block
        └── faq-block.php        # FAQ accordion block
```

### Assets Structure
```
assets/
├── css/
│   ├── tailwind.css            # Tailwind base
│   ├── components.css          # Custom components
│   ├── animations.css          # GSAP animations
│   └── responsive.css          # Media queries
├── js/
│   ├── main.js                 # Main JavaScript
│   ├── animations.js           # GSAP animations
│   ├── tabs.js                 # Industry tabs
│   ├── slider.js               # Testimonials slider
│   ├── smooth-scroll.js        # Smooth scrolling
│   └── menu-enhancements.js    # Additional menu customizations (if needed)
├── images/
│   ├── logos/                  # Client logos
│   ├── icons/                  # SVG icons
│   ├── platforms/              # Platform illustrations
│   └── hero/                   # Hero section assets
└── fonts/
    └── inter/                  # Inter font files (fallback)
```

---

## Tailwind Configuration

### Custom Colors (Base.vn inspired)
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'base': {
          'primary': '#000000',      // Main black
          'secondary': '#FFFFFF',    // Pure white
          'accent': '#0066FF',       // Base blue (estimated)
          'gray': {
            '50': '#F9FAFB',
            '100': '#F3F4F6',
            '200': '#E5E7EB',
            '300': '#D1D5DB',
            '400': '#9CA3AF',
            '500': '#6B7280',
            '600': '#4B5563',
            '700': '#374151',
            '800': '#1F2937',
            '900': '#111827',
          }
        }
      },
      fontFamily: {
        'inter': ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'hero': ['3.5rem', { lineHeight: '1.1' }],
        'section': ['2.5rem', { lineHeight: '1.2' }],
        'card': ['1.25rem', { lineHeight: '1.4' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-up': 'slideUp 0.8s ease-out',
        'float': 'float 3s ease-in-out infinite',
      }
    }
  }
}
```

### Custom Components
```css
/* components.css */

/* Max Mega Menu Plugin Overrides */
.mega-menu-wrap,
.mega-menu-wrap .mega-menu {
  @apply font-inter;
}

#mega-menu-wrap-primary #mega-menu-primary {
  @apply bg-white border-b border-gray-100;
}

#mega-menu-wrap-primary #mega-menu-primary > li.mega-menu-item > a.mega-menu-link {
  @apply text-base-primary font-medium hover:text-base-accent transition-colors duration-200;
}

#mega-menu-wrap-primary #mega-menu-primary > li.mega-menu-item.mega-current-menu-item > a.mega-menu-link,
#mega-menu-wrap-primary #mega-menu-primary > li.mega-menu-item > a.mega-menu-link:hover {
  @apply text-base-accent;
}

/* Mega Menu Dropdown Styling */
.mega-menu-wrap .mega-sub-menu {
  @apply bg-white shadow-2xl border-t border-gray-100 rounded-b-lg;
}

.mega-menu-wrap .mega-sub-menu li.mega-menu-item a.mega-menu-link {
  @apply text-gray-700 hover:text-base-accent hover:bg-gray-50 transition-all duration-200;
}

/* Platform Cards in Mega Menu */
.platform-card {
  @apply bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1;
}

.industry-tab {
  @apply px-6 py-3 rounded-full border border-gray-200 hover:border-base-accent hover:text-base-accent transition-all duration-200;
}

.industry-tab.active {
  @apply bg-base-accent text-white border-base-accent;
}

.cta-button {
  @apply bg-base-accent text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-all duration-200 transform hover:scale-105;
}
```

---

## Max Mega Menu Configuration Strategy

### Plugin Setup
1. **Installation & Activation**
   - Install Max Mega Menu plugin từ WordPress repository
   - Activate plugin và assign to Primary menu location
   - Configure general settings (theme, effect, transitions)

2. **Menu Structure** (6 Platforms)
   - WORK+ Platform
   - HRM+ Platform  
   - INFO+ Platform
   - FINANCE+ Platform
   - CRM Platform
   - Solutions (additional)

3. **Styling Approach**
   - Sử dụng plugin's built-in theme làm base
   - Override với custom CSS trong `assets/css/components.css`
   - Áp dụng Tailwind utility classes qua `@apply` directive
   - Đảm bảo responsive design cho mobile/tablet

4. **Custom CSS Targets**
   ```css
   /* Key selectors to override */
   .mega-menu-wrap                    /* Container wrapper */
   #mega-menu-primary                 /* Main menu */
   .mega-menu-item                    /* Menu items */
   .mega-menu-link                    /* Menu links */
   .mega-sub-menu                     /* Dropdown panels */
   .mega-menu-column                  /* Column layout */
   ```

5. **Integration với Base.vn Design**
   - Typography: Inter font family
   - Colors: Black (#000000), White (#FFFFFF), Blue accent (#0066FF)
   - Spacing: Consistent padding/margins theo Base.vn
   - Hover effects: Smooth color transitions
   - Icons: SVG icons cho platform categories

---

## Dynamic Sections với ACF

### Platform Management
```php
// ACF Field Groups
'platforms' => [
    'name' => 'Platforms',
    'fields' => [
        'platform_title' => 'text',
        'platform_description' => 'textarea',
        'platform_icon' => 'image',
        'platform_apps' => 'repeater' => [
            'app_name' => 'text',
            'app_description' => 'text',
            'app_icon' => 'image',
            'app_link' => 'url'
        ]
    ]
]
```

### Industry Sectors
```php
'industries' => [
    'name' => 'Industries',
    'fields' => [
        'industry_name' => 'text',
        'industry_icon' => 'image',
        'industry_description' => 'textarea',
        'industry_image' => 'image',
        'industry_stats' => 'repeater' => [
            'stat_number' => 'text',
            'stat_label' => 'text'
        ],
        'industry_clients' => 'repeater' => [
            'client_logo' => 'image',
            'client_name' => 'text'
        ]
    ]
]
```

### Testimonials
```php
'testimonials' => [
    'name' => 'Testimonials',
    'fields' => [
        'client_name' => 'text',
        'client_position' => 'text',
        'client_company' => 'text',
        'client_photo' => 'image',
        'company_logo' => 'image',
        'testimonial_text' => 'textarea',
        'key_metric' => 'text',
        'metric_description' => 'text'
    ]
]
```

---

## Phân kỳ thực hiện

### Phase 1: Foundation Setup (Step 03)
**Timeline: 1-2 days**
- [x] WordPress environment setup
- [ ] Theme scaffolding
- [ ] Tailwind CSS integration
- [ ] Basic file structure
- [ ] ACF plugin installation & configuration

### Phase 2: Header & Navigation (Step 04)
- [ ] Header layout với logo
- [ ] Cài đặt và kích hoạt Max Mega Menu plugin
- [ ] Cấu hình Max Mega Menu settings (theme location, menu style)
- [ ] Tạo menu structure với 6 platforms trong WordPress admin
- [ ] Custom CSS/Tailwind để style mega menu theo Base.vn design
  - [ ] Override plugin default styles
  - [ ] Áp dụng Base.vn color scheme (black/white/blue)
  - [ ] Custom hover effects và transitions
  - [ ] Typography matching (Inter font)
- [ ] Mobile responsive navigation
- [ ] Smooth animations với GSAP (nếu cần)
- [ ] Search functionality integration

### Phase 3: Hero Section (Step 05)
**Timeline: 1-2 days**
- [ ] Hero layout với video background
- [ ] CTA buttons
- [ ] Animated text effects
- [ ] Responsive design
- [ ] Performance optimization

### Phase 4: Platform Showcase (Step 06)
**Timeline: 3-4 days**
- [ ] 5 platform cards với tabs
- [ ] Interactive hover effects
- [ ] Icon animations
- [ ] ACF integration cho dynamic content
- [ ] Mobile carousel view

### Phase 5: Industry Sections (Step 07)
**Timeline: 2-3 days**
- [ ] Industry tabs (8 main sectors)
- [ ] Dynamic content loading
- [ ] Client logos slider
- [ ] Statistics animations
- [ ] Filtering functionality

### Phase 6: Content Blocks (Step 08)
**Timeline: 2-3 days**
- [ ] AI section với interactive elements
- [ ] Digital transformation journey (4 steps)
- [ ] Integration showcase (apps grid)
- [ ] Awards & certifications carousel

### Phase 7: Testimonials & Social Proof (Step 09)
**Timeline: 1-2 days**
- [ ] Customer testimonials slider
- [ ] Company logos grid
- [ ] Statistics counters
- [ ] Case study previews

### Phase 8: Footer & Final Touches (Step 10)
**Timeline: 1-2 days**
- [ ] Multi-column footer
- [ ] Contact information
- [ ] Social media links
- [ ] Newsletter signup
- [ ] Legal pages

### Phase 9: Performance & SEO (Step 11)
**Timeline: 1-2 days**
- [ ] Image optimization
- [ ] CSS/JS minification
- [ ] SEO meta tags
- [ ] Schema markup
- [ ] Page speed optimization

### Phase 10: Testing & Launch (Step 12)
**Timeline: 1-2 days**
- [ ] Cross-browser testing
- [ ] Mobile responsiveness
- [ ] Accessibility compliance
- [ ] Content population
- [ ] Final deployment

---

## Platform Content Management Strategy

### Hệ sinh thái ứng dụng (Base.vn style)
Sử dụng ACF để quản lý các nhóm nội dung tương tự Base.vn:

1. **WORK+ Platform**
   - Project Management tools
   - Workflow automation
   - Team collaboration

2. **HRM+ Platform**
   - Recruitment solutions
   - Employee management
   - Payroll systems

3. **INFO+ Platform**
   - Internal communication
   - Document management
   - Knowledge base

4. **FINANCE+ Platform**
   - Financial management
   - Expense tracking
   - Asset management

5. **CRM Platform**
   - Customer management
   - Sales pipeline
   - Marketing automation

### WordPress Custom Post Types
```php
// Custom Post Types for Platform Management
register_post_type('platforms');
register_post_type('applications');
register_post_type('industries');
register_post_type('testimonials');
register_post_type('case_studies');
```

---

## Technical Requirements

### Required Plugins
- Advanced Custom Fields Pro
- Max Mega Menu (navigation)
- Yoast SEO
- WP Rocket (caching)
- Smush (image optimization)
- Contact Form 7

### JavaScript Libraries
- GSAP (animations)
- Swiper.js (sliders)
- AOS (scroll animations)
- Lottie (micro-interactions)

### Performance Targets
- Page Speed Score: 90+
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Cumulative Layout Shift: < 0.1

---

## Next Steps
1. Confirm project plan approval
2. Proceed to Step 03: Scaffolding & Assets
3. Begin theme development following the phased approach
4. Regular progress reviews and adjustments

**Estimated Total Timeline: 15-20 days**
**Complexity Level: High (Enterprise-grade landing page)**