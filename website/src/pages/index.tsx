import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

const translations = {
  en: {
    tagline: 'Universal HTML to Image Converter',
    description: 'Cross-platform HTML to image conversion tool built on Playwright',
    getStarted: 'Get Started',
    github: 'GitHub',
    quickStart: 'Quick Start',
    features: {
      highResolution: { title: 'High Resolution', description: 'Custom DPR support with 3.0x default scaling for crystal clear output' },
      multiBrowser: { title: 'Multi-Browser', description: 'Chromium, Firefox, and WebKit engines available for different rendering needs' },
      batchProcessing: { title: 'Batch Processing', description: 'Convert multiple files with configurable parallel workers' },
      flexibleConfig: { title: 'Flexible Configuration', description: 'Multiple output formats, size presets, and wait strategies' },
    },
  },
  'zh-Hans': {
    tagline: '通用 HTML 转图片工具',
    description: '跨平台 HTML 转图片工具，基于 Playwright 构建',
    getStarted: '开始使用',
    github: 'GitHub',
    quickStart: '快速开始',
    features: {
      highResolution: { title: '高分辨率输出', description: '自定义 DPR，默认 3.0 倍缩放，输出清晰锐利' },
      multiBrowser: { title: '多浏览器支持', description: 'Chromium、Firefox、WebKit 引擎，满足不同渲染需求' },
      batchProcessing: { title: '批量处理', description: '支持批量转换多文件，可配置并行处理' },
      flexibleConfig: { title: '灵活配置', description: '多种输出格式、尺寸预设和等待策略' },
    },
  },
};

function HomepageHeader() {
  const { i18n } = useDocusaurusContext();
  const t = translations[i18n.currentLocale] || translations.en;

  return (
    <header className={styles.hero}>
      <div className="container">
        <h1 className={styles.title}>html2png</h1>
        <p className={styles.tagline}>
          {t.tagline.split(' ').map((word, index) => (
            <span key={index} style={{ animationDelay: `${index * 0.15}s` }}>
              {word}
            </span>
          ))}
        </p>
        <p className={styles.description}>
          {t.description}
        </p>
        <div className={styles.buttons}>
          <Link className="button button--primary" to="/docs/intro">
            {t.getStarted}
          </Link>
          <Link
            className="button button--secondary"
            to="https://github.com/Youpen-y/html2png"
          >
            {t.github}
          </Link>
        </div>
      </div>
    </header>
  );
}

function Feature({ title, description }: { title: string; description: string }) {
  return (
    <div className="col col--6">
      <div className={styles.featureCard}>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home() {
  const { i18n } = useDocusaurusContext();
  const t = translations[i18n.currentLocale] || translations.en;

  return (
    <Layout>
      <HomepageHeader />
      <main className={styles.main}>
        <div className="container">
          <section className={styles.features}>
            <div className="row">
              <Feature
                title={t.features.highResolution.title}
                description={t.features.highResolution.description}
              />
              <Feature
                title={t.features.multiBrowser.title}
                description={t.features.multiBrowser.description}
              />
            </div>
            <div className="row">
              <Feature
                title={t.features.batchProcessing.title}
                description={t.features.batchProcessing.description}
              />
              <Feature
                title={t.features.flexibleConfig.title}
                description={t.features.flexibleConfig.description}
              />
            </div>
          </section>

          <section className={styles.installation}>
            <h2>{t.quickStart}</h2>
            <div className={styles.codeBlock}>git clone https://github.com/Youpen-y/html2png.git</div>
            <div className={styles.codeBlock}>cd html2png && uv sync</div>
            <div className={styles.codeBlock}>uv run playwright install chromium</div>
            <div className={styles.codeBlock}>uv run html2png convert input.html -o output.png</div>
          </section>
        </div>
      </main>
    </Layout>
  );
}
