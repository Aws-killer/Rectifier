import {Series} from 'remotion';
import React from 'react';
import {Video, staticFile, useVideoConfig} from 'remotion';
import videoSequences from './Assets/VideoSequences.json';
export default function VideoStream() {
	const {fps} = useVideoConfig();
	return (
		<Series
			style={{
				color: 'white',
				position: 'absolute',
				zIndex: 0,
			}}
		>
			{videoSequences.map((entry, index) => {
				return (
					<Series.Sequence
						from={fps * entry.start}
						durationInFrames={fps * (entry.end - entry.start)}
					>
						<Video {...entry.props} src={staticFile(entry.name)} />
					</Series.Sequence>
				);
			})}
		</Series>
	);
}
