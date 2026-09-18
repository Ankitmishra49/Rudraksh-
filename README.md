# LUSHI AI Global Commerce Dashboard

A modern, AI-powered global commerce automation platform built with Next.js, React, and TypeScript. This dashboard provides real-time product intelligence, affiliate management, and automated commerce operations.

## Features

- 🌍 **Global Market Intelligence**: Monitor products across multiple markets
- 🤖 **AI Automation Agents**: Scout, Content, Link, and Guard AI agents for automated workflows
- 📊 **Real-Time Analytics**: Track products, clicks, conversions, and commissions
- 🎯 **Product Opportunities**: Discover high-potential affiliate products ranked by demand and commission
- ⚡ **Autopilot Mode**: Toggle automated operations on/off
- 🎨 **Modern UI**: Dark theme with responsive design
- ♿ **Accessible**: WCAG compliant components

## Tech Stack

- **Framework**: Next.js 14.2.5
- **Language**: TypeScript 5+
- **Styling**: CSS3 with CSS Variables
- **UI Components**: Lucide React Icons
- **Node**: 18+

## Getting Started

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

1. **Clone or extract the repository**
   ```bash
   cd lushi-ai-global-commerce
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Create optimized production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint (if configured)

## Project Structure

```
├── app/
│   ├── page.tsx          # Main dashboard page
│   ├── layout.tsx        # Root layout with metadata
│   └── globals.css       # Global styles
├── next.config.mjs       # Next.js configuration
├── tsconfig.json         # TypeScript configuration
├── package.json          # Dependencies and scripts
└── README.md            # This file
```

## Development

### Code Quality

- **TypeScript Strict Mode**: Enabled for better type safety
- **Component Structure**: Organized with proper TypeScript interfaces
- **Styling**: CSS with variables for consistent theming
- **Icons**: Lucide React for scalable SVG icons

### Customization

1. **Colors**: Edit CSS variables in `globals.css` for theme customization
2. **Content**: Update product data and agent status in `page.tsx`
3. **Navigation**: Modify `navItems` array to add/remove sections

## Integration Guide

Before deploying to production, integrate the following services:

### Required Integrations

- **Authentication**: Implement user login/signup system
- **Database**: Connect to your backend database
- **Affiliate APIs**: Integrate affiliate networks (Amazon Associates, CJ Affiliate, etc.)
- **Payment Processing**: Setup payment/payout services
- **AI Providers**: Connect Claude API or other AI services
- **Analytics**: Integrate analytics tracking

### Example Integration Point (page.tsx)

```typescript
// Add your API calls here
const fetchProducts = async () => {
  const response = await fetch('/api/products');
  return response.json();
};
```

## Compliance & Legal

⚠️ **Important**: This is a frontend starter template only.

- ✅ Never scrape or automate marketplaces against their terms of service
- ✅ Always use approved affiliate APIs and networks
- ✅ Ensure all affiliate links follow FTC disclosure guidelines
- ✅ Implement proper data privacy and GDPR compliance
- ✅ Verify all commission structures with affiliate partners

## Performance

- Optimized bundle size
- Server-side rendering ready
- Image optimization configured
- CSS minification
- Fast page loads with Next.js optimization

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Other Platforms

This project can be deployed to any platform supporting Node.js:
- AWS Amplify
- Netlify
- DigitalOcean
- Heroku
- Docker containers

## Troubleshooting

### Port 3000 Already in Use

```bash
npm run dev -- -p 3001
```

### Clear Next.js Cache

```bash
rm -rf .next node_modules package-lock.json
npm install
```

### TypeScript Errors

Ensure TypeScript is up to date:

```bash
npm install -D typescript@latest
```

## Contributing

For improvements and bug fixes, please ensure:
- Code follows the existing style
- TypeScript strict mode is satisfied
- No console warnings or errors

## License

© 2026 LUSHI AI - Commerce automation platform

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Next.js documentation: https://nextjs.org/docs
3. Check TypeScript documentation: https://www.typescriptlang.org/docs
