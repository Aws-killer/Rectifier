import {Series} from 'remotion';
import React from 'react';
import {Video, staticFile, useVideoConfig} from 'remotion';
import videoSequences from './Assets/VideoSequences.json';
import {TransitionSeries} from '@remotion/transitions';

const VideoStream = React.memo(() => {
	const {fps} = useVideoConfig();
	return (
		<TransitionSeries
			style={{
				position: 'absolute',
				zIndex: 1,
			}}
		>
			{videoSequences.map((entry, index) => {
				return (
					<TransitionSeries.Sequence
						key={index}
						from={fps * entry.start}
						durationInFrames={fps * (entry.end - entry.start)}
					>
						<VideoX entry={entry} />
					</TransitionSeries.Sequence>
				);
			})}
		</TransitionSeries>
	);
});

const VideoX = React.memo(({entry}) => {
	return (
		<Video
			startFrom={entry.props.startFrom}
			endAt={entry.props.endAt}
			volume={entry.props.volume}
			src={staticFile(entry.name)}
		/>
	);
});

export default VideoStream;
