import {Series} from 'remotion';
import React, {useMemo} from 'react';
import {staticFile, useVideoConfig, Audio} from 'remotion';
import audioSequences from './Assets/AudioSequences.json';
import {TransitionSeries} from '@remotion/transitions';

const AudioStream = React.memo(() => {
	const {fps} = useVideoConfig();

	const audioComponents = useMemo(() => {
		return audioSequences.map((entry, index) => (
			<TransitionSeries.Sequence
				key={index}
				from={fps * entry.start}
				durationInFrames={fps * (entry.end - entry.start)}
			>
				<AudioX entry={entry} />
			</TransitionSeries.Sequence>
		));
	}, [fps]);

	return (
		<TransitionSeries
			style={{
				color: 'white',
				position: 'absolute',
				zIndex: 0,
			}}
		>
			{audioComponents}
		</TransitionSeries>
	);
});

const AudioX = React.memo(({entry}) => {
	return <Audio {...entry.props} src={staticFile(entry.name)} />;
});

export default AudioStream;
