import {Series} from 'remotion';
import React from 'react';
import {staticFile, useVideoConfig, Audio} from 'remotion';
import audioSequences from './Assets/AudioSequences.json';
export default function AudioStream() {
	const {fps} = useVideoConfig();
	return (
		<Series
			style={{
				color: 'white',
				position: 'absolute',
				zIndex: 0,
			}}
		>
			{audioSequences.map((entry, index) => {
				return (
					<Series.Sequence
						from={fps * entry.start}
						durationInFrames={fps * (entry.end - entry.start)}
					>
						<Audio {...entry.props} src={staticFile(entry.name)} />
					</Series.Sequence>
				);
			})}
		</Series>
	);
}
