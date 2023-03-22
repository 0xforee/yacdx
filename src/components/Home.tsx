import React, { Suspense } from 'react';
import { useTranslation } from 'react-i18next';

import ContentHeader from './ContentHeader';
import s0 from './Home.module.scss';
import Loading from './Loading';
import TrafficNow from './TrafficNow';
import AllChart from './AllChart';

export default function Home() {
  const { t } = useTranslation();
  return (
    <div>
      <ContentHeader title={t('Overview')} />
      <div className={s0.root}>
        <div>
          <TrafficNow />
        </div>
        <div >
          <Suspense fallback={<Loading height="400px" />}>
            <AllChart/>
          </Suspense>
        </div>
      </div>
    </div>
  );
}
