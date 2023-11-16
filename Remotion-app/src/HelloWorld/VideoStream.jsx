import {Series} from 'remotion';
import React from 'react';
import {Video, staticFile, useVideoConfig, Sequence} from 'remotion';
import videoSequences from './Assets/VideoSequences.json';
import {TransitionSeries} from '@remotion/transitions';
export default function VideoStream() {
	const {fps} = useVideoConfig();
	return (
		<div
			style={{
				color: 'white',
				position: 'absolute',
				zIndex: 0,
			}}
		>
			{videoSequences.map((entry, index) => {
				return (
					<Sequence
						key={index}
						from={fps * entry.start}
						durationInFrames={fps * (entry.end - entry.start)}
					>
						<Video {...entry.props} src={staticFile(entry.name)} />
					</Sequence>
				);
			})}
		</div>
	);
}
